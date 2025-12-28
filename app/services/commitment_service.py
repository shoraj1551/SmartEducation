"""
Commitment Service for Feature 3: Hard Commitment Mode
Handles commitment lifecycle, violation detection, and consequences
"""
from datetime import datetime, timedelta
from app.models import Commitment, CommitmentViolation, LearningItem, User, AccountabilityPartner
from mongoengine.errors import DoesNotExist


class CommitmentService:
    """Service for managing commitments and enforcing discipline"""
    
    # Consequence severity levels
    SEVERITY_WARNING = 1
    SEVERITY_STREAK_RESET = 2
    SEVERITY_CONTENT_LOCKOUT_24H = 3
    SEVERITY_COURSE_RESTRICTION = 4
    SEVERITY_PARTNER_NOTIFICATION = 5
    
    @staticmethod
    def create_commitment(user_id, learning_item_id, commitment_data):
        """
        Create a new commitment with validation
        
        Args:
            user_id: User ID
            learning_item_id: Learning item ID
            commitment_data: Dictionary with commitment details
            
        Returns:
            Commitment object
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
            
            try:
                item = LearningItem.objects.get(id=learning_item_id)
            except DoesNotExist:
                # Try to find it as a Bookmark and auto-import
                from app.models import Bookmark
                from app.services.inbox_service import InboxService
                try:
                    # Verify bookmark exists and belongs to user
                    Bookmark.objects.get(id=learning_item_id, user_id=user)
                    # Import it -> Returns new LearningItem
                    item = InboxService.import_from_bookmark(user, learning_item_id)
                except DoesNotExist:
                    raise ValueError("Learning item or bookmark not found")
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Phase 33: Enforce 2-commitment maximum
        active_count = Commitment.objects(user_id=user, status='active').count()
        if active_count >= 2:
            active_commitments = Commitment.objects(user_id=user, status='active')
            commitment_titles = [c.learning_item_id.title for c in active_commitments]
            raise ValueError(
                f"Maximum 2 active commitments allowed. You currently have: {', '.join(commitment_titles)}. "
                f"Please complete or break an existing commitment first."
            )
        
        # Check if commitment already exists for this item
        existing = Commitment.objects(
            user_id=user,
            learning_item_id=item,
            status='active'
        ).first()
        
        if existing:
            raise ValueError("Active commitment already exists for this item")
        
        # Validate commitment is realistic
        target_date = commitment_data.get('target_completion_date')
        daily_minutes = commitment_data.get('daily_study_minutes')
        study_days = commitment_data.get('study_days_per_week', 5)
        
        if not target_date or not daily_minutes:
            raise ValueError("target_completion_date and daily_study_minutes are required")
        
        # Check if target date is realistic
        if isinstance(target_date, str):
             # Handle string date format if coming from JSON
             try:
                 target_date = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
             except:
                 pass # Let downstream handle or fail if object

        days_available = (target_date - datetime.utcnow()).days
        if days_available < 1:
            raise ValueError("Target date must be in the future")
            
        # ---------------------------------------------------------
        # REALITY CHECK (Feature 3 Enhancement)
        # ---------------------------------------------------------
        from app.services.reality_service import RealityService
        reality_check = RealityService.check_feasibility(
            user, item.id, target_date, daily_minutes, study_days
        )
        
        if not reality_check['is_feasible']:
             raise ValueError(f"Reality Check Failed: {reality_check['message']}")
        
        # Create commitment
        commitment = Commitment(
            user_id=user,
            learning_item_id=item,
            target_completion_date=target_date,
            daily_study_minutes=daily_minutes,
            study_days_per_week=study_days,
            has_accountability_partner=commitment_data.get('has_accountability_partner', False),
            accountability_partner_email=commitment_data.get('accountability_partner_email', '')
        )
        
        commitment.lock()
        
        # ---------------------------------------------------------
        # AUTO-BREAKDOWN (Feature 4 Enhancement)
        # ---------------------------------------------------------
        # Automatically generate daily tasks for this commitment
        try:
            from app.services.breakdown_service import AutoBreakdownService
            AutoBreakdownService.generate_daily_tasks(commitment.id)
        except Exception as e:
            # Non-blocking error logging (Plan generation shouldn't fail commitment creation)
            print(f"Stats generation failed: {e}")
        
        # ---------------------------------------------------------
        # GOOGLE CALENDAR SYNC (Phase 34.2)
        # ---------------------------------------------------------
        # Automatically sync to Google Calendar if connected
        try:
            if user.google_calendar_connected:
                from app.services.google_calendar_service import GoogleCalendarService
                GoogleCalendarService.sync_commitment_to_google(commitment)
        except Exception as e:
            # Non-blocking error logging
            print(f"Google Calendar sync failed: {e}")

        return commitment
    
    @staticmethod
    def daily_check_in(commitment_id, study_duration_minutes):
        """
        Daily check-in for a commitment
        
        Args:
            commitment_id: Commitment ID
            study_duration_minutes: How many minutes studied today
            
        Returns:
            Updated commitment with streak info
        """
        try:
            commitment = Commitment.objects.get(id=commitment_id)
        except DoesNotExist:
            raise ValueError("Commitment not found")
        
        if commitment.status != 'active':
            raise ValueError("Commitment is not active")
        
        # Check if already checked in today
        if commitment.last_check_in:
            last_check_date = commitment.last_check_in.date()
            today = datetime.utcnow().date()
            if last_check_date == today:
                raise ValueError("Already checked in today")
        
        # Validate study duration meets commitment
        if study_duration_minutes >= commitment.daily_study_minutes:
            # Successful check-in
            commitment.current_streak += 1
            if commitment.current_streak > commitment.longest_streak:
                commitment.longest_streak = commitment.current_streak
        else:
            # Incomplete session - create violation
            CommitmentService._create_violation(
                commitment,
                'incomplete_duration',
                severity=CommitmentService.SEVERITY_WARNING,
                consequence='warning'
            )
        
        commitment.last_check_in = datetime.utcnow()
        commitment.save()
        
        return commitment
    
    @staticmethod
    def detect_missed_sessions(user_id=None):
        """
        Detect missed sessions for all active commitments
        Run as a daily cron job
        
        Args:
            user_id: Optional user ID to check specific user
            
        Returns:
            List of violations created
        """
        query = {'status': 'active'}
        if user_id:
            try:
                if isinstance(user_id, str):
                    user = User.objects.get(id=user_id)
                else:
                    user = user_id
                query['user_id'] = user
            except DoesNotExist:
                return []
        
        commitments = Commitment.objects(**query)
        violations = []
        
        for commitment in commitments:
            # Check if last check-in was yesterday or earlier
            if commitment.last_check_in:
                days_since_check_in = (datetime.utcnow() - commitment.last_check_in).days
                
                if days_since_check_in >= 1:
                    # Missed session detected
                    violation = CommitmentService._handle_missed_session(commitment, days_since_check_in)
                    if violation:
                        violations.append(violation)
            else:
                # Never checked in - first day grace period
                days_since_creation = (datetime.utcnow() - commitment.created_at).days
                if days_since_creation >= 2:
                    violation = CommitmentService._handle_missed_session(commitment, days_since_creation)
                    if violation:
                        violations.append(violation)
        
        return violations
    
    @staticmethod
    def _handle_missed_session(commitment, days_missed):
        """Handle a missed session with appropriate consequences"""
        # Get violation history
        recent_violations = CommitmentViolation.objects(
            commitment_id=commitment,
            violation_date__gte=datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Determine severity based on violation history
        if recent_violations == 0:
            # First violation - grace period
            severity = CommitmentService.SEVERITY_WARNING
            consequence = 'warning'
            is_grace = True
        elif recent_violations == 1:
            # Second violation - streak reset
            severity = CommitmentService.SEVERITY_STREAK_RESET
            consequence = 'streak_reset'
            is_grace = False
            commitment.current_streak = 0
            commitment.save()
        elif recent_violations == 2:
            # Third violation - 24h content lockout
            severity = CommitmentService.SEVERITY_CONTENT_LOCKOUT_24H
            consequence = 'content_lockout_24h'
            is_grace = False
        elif recent_violations >= 3:
            # Multiple violations - notify partner and restrict course
            severity = CommitmentService.SEVERITY_PARTNER_NOTIFICATION
            consequence = 'partner_notification'
            is_grace = False
            
            if commitment.has_accountability_partner:
                CommitmentService._notify_accountability_partner(commitment)
        else:
            severity = CommitmentService.SEVERITY_WARNING
            consequence = 'warning'
            is_grace = False
        
        return CommitmentService._create_violation(
            commitment,
            'missed_session',
            severity=severity,
            consequence=consequence,
            is_grace=is_grace,
            metadata={'days_missed': days_missed}
        )
    
    @staticmethod
    def _create_violation(commitment, violation_type, severity, consequence, is_grace=False, metadata=None):
        """Create a violation record"""
        violation = CommitmentViolation(
            commitment_id=commitment,
            user_id=commitment.user_id,
            violation_type=violation_type,
            severity_level=severity,
            consequence_applied=consequence,
            is_grace_period=is_grace,
            violation_metadata=metadata or {}
        )
        
        # Set consequence duration
        if consequence == 'content_lockout_24h':
            violation.consequence_duration_hours = 24
        elif consequence == 'course_restriction':
            violation.consequence_duration_hours = 48
        
        violation.save()
        return violation
    
    
    @staticmethod
    def _notify_accountability_partner(commitment):
        """Send notification to accountability partner and user about missed commitment"""
        from flask_mail import Message
        from flask import current_app
        from app import mail
        
        user = commitment.user_id
        
        # Send email to user about missed commitment
        try:
            user_msg = Message(
                subject='⚠️ Commitment Alert: Missed Session Detected',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            user_msg.html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #ef4444;">Commitment Alert</h2>
                <p>You missed a session for your commitment:</p>
                <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong>{commitment.learning_item_id.title}</strong><br>
                    Daily Target: {commitment.daily_study_minutes} minutes
                </div>
                <p>Remember your commitment! Get back on track today.</p>
                <p style="color: #64748b; font-size: 0.9em;">
                    Current Streak: {commitment.current_streak} days<br>
                    Longest Streak: {commitment.longest_streak} days
                </p>
            </div>
            """
            mail.send(user_msg)
        except Exception as e:
            print(f"Failed to send user notification: {e}")
        
        # Send to accountability partner if exists
        if commitment.has_accountability_partner and commitment.accountability_partner_email:
            try:
                partner_msg = Message(
                    subject=f'Accountability Alert: {user.name} missed a commitment session',
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[commitment.accountability_partner_email]
                )
                partner_msg.html = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Accountability Partner Alert</h2>
                    <p>{user.name} missed a session for their commitment:</p>
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <strong>{commitment.learning_item_id.title}</strong>
                    </div>
                    <p>As their accountability partner, please check in with them.</p>
                </div>
                """
                mail.send(partner_msg)
            except Exception as e:
                print(f"Failed to send partner notification: {e}")

    
    @staticmethod
    def get_active_commitments(user_id):
        """Get all active commitments for a user"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        return list(Commitment.objects(user_id=user, status='active'))
    
    @staticmethod
    def get_violations(user_id, days=7):
        """Get recent violations for a user"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        since_date = datetime.utcnow() - timedelta(days=days)
        return list(CommitmentViolation.objects(
            user_id=user,
            violation_date__gte=since_date
        ).order_by('-violation_date'))
    
    @staticmethod
    def is_user_locked_out(user_id):
        """Check if user is currently locked out from adding content"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return False
        
        # Check for active lockout violations
        active_lockouts = CommitmentViolation.objects(
            user_id=user,
            consequence_applied__in=['content_lockout_24h', 'course_restriction'],
            is_resolved=False
        )
        
        for violation in active_lockouts:
            # Check if lockout is still active
            lockout_end = violation.violation_date + timedelta(hours=violation.consequence_duration_hours)
            if datetime.utcnow() < lockout_end:
                return True
        
        return False
    
    @staticmethod
    def modify_commitment(commitment_id, new_data):
        """
        Modify a commitment (limited modifications allowed)
        
        Args:
            commitment_id: Commitment ID
            new_data: New commitment data
            
        Returns:
            Updated commitment
        """
        try:
            commitment = Commitment.objects.get(id=commitment_id)
        except DoesNotExist:
            raise ValueError("Commitment not found")
        
        if commitment.modification_count >= commitment.max_modifications:
            raise ValueError(f"Maximum modifications ({commitment.max_modifications}) reached")
        
        # Allow modification
        if 'target_completion_date' in new_data:
            commitment.target_completion_date = new_data['target_completion_date']
        if 'daily_study_minutes' in new_data:
            commitment.daily_study_minutes = new_data['daily_study_minutes']
        
        commitment.modification_count += 1
        commitment.save()
        
        return commitment
    
    @staticmethod
    def break_commitment(commitment_id, user_id):
        """
        Break/abandon a commitment with reputation penalty (Phase 33)
        
        Args:
            commitment_id: Commitment ID
            user_id: User ID (for ownership verification)
            
        Returns:
            Dictionary with updated commitment and reputation info
        """
        try:
            commitment = Commitment.objects.get(id=commitment_id)
        except DoesNotExist:
            raise ValueError("Commitment not found")
        
        # Verify ownership
        if str(commitment.user_id.id) != str(user_id):
            raise ValueError("Access denied")
        
        if commitment.status != 'active':
            raise ValueError(f"Cannot break commitment with status: {commitment.status}")
        
        # Mark as broken
        commitment.status = 'broken'
        commitment.broken_at = datetime.utcnow()
        commitment.save()
        
        # Phase 34.2: Delete from Google Calendar if synced
        try:
            if commitment.user_id.google_calendar_connected:
                from app.services.google_calendar_service import GoogleCalendarService
                GoogleCalendarService.delete_google_event(commitment)
        except Exception as e:
            print(f"Failed to delete Google Calendar event: {e}")
        
        # Apply reputation penalty
        user = commitment.user_id
        REPUTATION_PENALTY = 50  # Deduct 50 points for breaking commitment
        user.reputation_score = max(0, user.reputation_score - REPUTATION_PENALTY)
        user.save()
        
        return {
            'commitment': commitment.to_dict(),
            'reputation_score': user.reputation_score,
            'penalty_applied': REPUTATION_PENALTY,
            'message': f'Commitment broken. Reputation decreased by {REPUTATION_PENALTY} points.'
        }
