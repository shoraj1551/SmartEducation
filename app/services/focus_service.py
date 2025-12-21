"""
Focus Mode Service for Feature 5: Single Focus Learning Mode
Handles focus session management and distraction prevention
"""
from datetime import datetime, timedelta
from app.models import FocusSession, LearningItem, DailyTask, User
from mongoengine.errors import DoesNotExist


class FocusModeService:
    """Service for managing focus mode sessions"""
    
    @staticmethod
    def activate_focus_mode(user_id, learning_item_id, daily_task_id=None):
        """
        Activate focus mode for a learning item
        
        Args:
            user_id: User ID
            learning_item_id: Learning item to focus on
            daily_task_id: Optional specific task to focus on
            
        Returns:
            FocusSession object
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
            
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("User or learning item not found")
        
        # Check if user already has an active focus session
        existing_session = FocusSession.objects(
            user_id=user,
            is_active=True
        ).first()
        
        if existing_session:
            raise ValueError("You already have an active focus session. Exit it first.")
        
        # Get daily task if provided
        task = None
        if daily_task_id:
            try:
                task = DailyTask.objects.get(id=daily_task_id)
            except DoesNotExist:
                pass
        
        # Create focus session
        session = FocusSession(
            user_id=user,
            learning_item_id=item,
            daily_task_id=task
        )
        session.save()
        
        return session
    
    @staticmethod
    def get_active_session(user_id):
        """Get user's active focus session"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return None
        
        return FocusSession.objects(user_id=user, is_active=True).first()
    
    @staticmethod
    def deactivate_focus_mode(session_id, reason='completed'):
        """
        Deactivate focus mode
        
        Args:
            session_id: Focus session ID
            reason: Reason for exit (completed, emergency_exit, timeout)
            
        Returns:
            Ended session
        """
        try:
            session = FocusSession.objects.get(id=session_id)
        except DoesNotExist:
            raise ValueError("Focus session not found")
        
        if not session.is_active:
            raise ValueError("Session is already ended")
        
        session.end_session(reason)
        return session
    
    @staticmethod
    def log_distraction_attempt(session_id, distraction_type, details=None):
        """
        Log a distraction attempt during focus mode
        
        Args:
            session_id: Focus session ID
            distraction_type: Type of distraction (navigation, new_tab, etc.)
            details: Additional details
        """
        try:
            session = FocusSession.objects.get(id=session_id)
            session.log_distraction(distraction_type, details)
            return session
        except DoesNotExist:
            raise ValueError("Focus session not found")
    
    @staticmethod
    def update_session_progress(session_id, tasks_completed=0, content_minutes=0):
        """Update progress during focus session"""
        try:
            session = FocusSession.objects.get(id=session_id)
            
            if tasks_completed:
                session.tasks_completed += tasks_completed
            if content_minutes:
                session.content_consumed_minutes += content_minutes
            
            session.save()
            return session
        except DoesNotExist:
            raise ValueError("Focus session not found")
    
    @staticmethod
    def get_focus_stats(user_id, days=30):
        """
        Get focus mode analytics for a user
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary with focus statistics
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return {}
        
        since_date = datetime.utcnow() - timedelta(days=days)
        sessions = FocusSession.objects(
            user_id=user,
            started_at__gte=since_date
        )
        
        total_sessions = sessions.count()
        completed_sessions = sessions.filter(exit_reason='completed').count()
        total_focus_time = sum(s.duration_minutes for s in sessions)
        total_distractions = sum(s.distraction_attempts for s in sessions)
        
        # Calculate effectiveness
        effectiveness = 0
        if total_sessions > 0:
            effectiveness = (completed_sessions / total_sessions) * 100
        
        # Calculate average session duration
        avg_duration = total_focus_time / total_sessions if total_sessions > 0 else 0
        
        # Calculate focus streak (consecutive days with focus sessions)
        focus_streak = FocusModeService._calculate_focus_streak(user)
        
        return {
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'total_focus_time_minutes': total_focus_time,
            'total_distractions': total_distractions,
            'effectiveness_percentage': round(effectiveness, 2),
            'average_session_duration': round(avg_duration, 2),
            'focus_streak_days': focus_streak,
            'distractions_per_session': round(total_distractions / total_sessions, 2) if total_sessions > 0 else 0
        }
    
    @staticmethod
    def _calculate_focus_streak(user):
        """Calculate consecutive days with focus sessions"""
        sessions = FocusSession.objects(user_id=user).order_by('-started_at')
        
        if not sessions:
            return 0
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for session in sessions:
            session_date = session.started_at.date()
            
            if session_date == current_date or session_date == current_date - timedelta(days=streak):
                if session_date < current_date:
                    streak += 1
                    current_date = session_date
            else:
                break
        
        return streak
