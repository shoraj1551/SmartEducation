"""
Database models for SmartEducation (MongoDB)
"""
from datetime import datetime
from mongoengine import (
    Document, StringField, BooleanField, DateTimeField, 
    IntField, ReferenceField, FloatField, ListField, DictField
)
import bcrypt

# We will initialize connection in app.py

class User(Document):
    """User model for authentication"""
    meta = {'collection': 'users'}
    
    name = StringField(max_length=100, required=True)
    email = StringField(max_length=120, required=True, unique=True)
    mobile = StringField(max_length=15, required=True, unique=True)
    password_hash = StringField(max_length=255, required=True)
    password_history = ListField(StringField(max_length=255), default=list)  # Store last 3 password hashes
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Gamification
    xp_total = IntField(default=0)
    level = IntField(default=1)
    
    # Onboarding / Learning Context (OLD - kept for backward compatibility)
    learning_goal = StringField(max_length=50) # upskill, switch, academic, hobby
    interests = ListField(StringField(max_length=50)) # tech, business, design, etc.
    commitment_level = StringField(max_length=20) # light, moderate, intensive
    expertise_level = StringField(max_length=20) # beginner, intermediate, advanced
    
    # NEW Survey Fields (IMPROVEMENT-001)
    user_role = StringField(max_length=50) # school, college, professional, freelancer, career_switcher, other
    learning_goals = ListField(StringField(max_length=50)) # upskilling, career_switch, exams, academic, personal, salary_growth
    learning_type = StringField(max_length=50) # competitive_exams, structured_courses, skill_based, general_knowledge, not_sure
    deadline_type = StringField(max_length=50) # hard_deadline, soft_deadline, consistency, not_sure
    daily_time_commitment = StringField(max_length=50) # 15_30_min, 30_60_min, 1_2_hours, 2plus_hours, weekends_only
    learning_blockers = ListField(StringField(max_length=50)) # lack_of_time, too_many_resources, lose_motivation, overwhelming, no_plan

    # Profile Fields
    job_title = StringField(max_length=100)
    bio = StringField()
    profile_picture = StringField(max_length=255)
    education_info = StringField()
    linkedin_url = StringField(max_length=255)
    github_url = StringField(max_length=255)
    website_url = StringField(max_length=255)
    
    # Settings & Preferences
    theme_preference = StringField(max_length=20, default='dark')
    email_notifications = BooleanField(default=True)
    mobile_notifications = BooleanField(default=True)
    marketing_emails = BooleanField(default=False)
    
    # New Engagement & Accessibility Prefs
    preferred_learning_time = StringField(max_length=20, default='morning')
    daily_reminders = BooleanField(default=True)
    ai_insights = BooleanField(default=True)
    community_milestones = BooleanField(default=False)
    reduced_motion = BooleanField(default=False)
    high_contrast = BooleanField(default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def check_password_in_history(self, password, count=3):
        """Check if password matches any of the last N passwords"""
        if not self.password_history:
            return False
        
        recent_passwords = self.password_history[-count:] if len(self.password_history) >= count else self.password_history
        
        for old_hash in recent_passwords:
            try:
                if bcrypt.checkpw(password.encode('utf-8'), old_hash.encode('utf-8')):
                    return True
            except Exception:
                # Skip invalid hashes
                continue
        return False
    
    def add_to_password_history(self, password_hash):
        """Add password hash to history, keeping only last 3"""
        if not self.password_history:
            self.password_history = []
        
        self.password_history.append(password_hash)
        
        # Keep only last 3 passwords
        if len(self.password_history) > 3:
            self.password_history = self.password_history[-3:]

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # Old survey fields
            'learning_goal': self.learning_goal,
            'interests': self.interests,
            'commitment_level': self.commitment_level,
            'expertise_level': self.expertise_level,
            # New survey fields (IMPROVEMENT-001)
            'user_role': self.user_role,
            'learning_goals': self.learning_goals,
            'learning_type': self.learning_type,
            'deadline_type': self.deadline_type,
            'daily_time_commitment': self.daily_time_commitment,
            'learning_blockers': self.learning_blockers,
            # Profile fields
            'job_title': self.job_title,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'education_info': self.education_info,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'website_url': self.website_url,
            'theme_preference': self.theme_preference,
            'email_notifications': self.email_notifications,
            'mobile_notifications': self.mobile_notifications,
            'marketing_emails': self.marketing_emails,
            'preferred_learning_time': self.preferred_learning_time,
            'daily_reminders': self.daily_reminders,
            'ai_insights': self.ai_insights,
            'community_milestones': self.community_milestones,
            'reduced_motion': self.reduced_motion,
            'high_contrast': self.high_contrast,
            'xp_total': self.xp_total,
            'level': self.level
        }


class OTP(Document):
    """OTP model for verification"""
    meta = {'collection': 'otps'}
    
    user_id = StringField() # Link to user ID or temp session ID
    email = StringField(max_length=120)
    mobile = StringField(max_length=15)
    otp_code = StringField(max_length=6, required=True)
    otp_type = StringField(max_length=20, required=True) # email_verification, mobile_verification, password_reset
    purpose = StringField(max_length=50) # inline_verification, registration, reset
    created_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField(required=True)
    is_used = BooleanField(default=False)
    attempts = IntField(default=0)
    
    def is_expired(self):
        """Check if OTP has expired"""
        return datetime.utcnow() > self.expires_at


class Activity(Document):
    """Activity log for user actions"""
    meta = {'collection': 'activities'}
    
    user_id = ReferenceField(User, required=True)
    activity_type = StringField(max_length=50, required=True) # login, bookmark, profile_update, etc.
    description = StringField(max_length=255)
    timestamp = DateTimeField(default=datetime.utcnow)
    metadata = DictField() # Additional context

    def to_dict(self):
        return {
            'id': str(self.id),
            'activity_type': self.activity_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


class Bookmark(Document):
    """Bookmark model for saved resources"""
    meta = {'collection': 'bookmarks'}
    
    user_id = ReferenceField(User, required=True)
    title = StringField(max_length=200, required=True)
    url = StringField(max_length=500, required=True)
    description = StringField()
    category = StringField(max_length=100) # tech, science, design, business
    is_educational = BooleanField(default=False) # AI-determined educational flag
    relevance_score = FloatField(default=0.0) # AI-calculated relevance
    added_at = DateTimeField(default=datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    
    # New Library Sync Fields
    source = StringField(max_length=50) # youtube, udemy, coursera, drive, manual
    resource_type = StringField(max_length=50) # video, course, document, book
    file_path = StringField() # For manually uploaded files
    topic = StringField(max_length=100) # Python, System Design, etc.
    is_uploaded = BooleanField(default=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'category': self.category,
            'is_educational': self.is_educational,
            'relevance_score': self.relevance_score,
            'added_at': self.added_at.isoformat(),
            'tags': self.tags,
            'source': self.source,
            'resource_type': self.resource_type,
            'topic': self.topic,
            'is_uploaded': self.is_uploaded
        }


class UserSession(Document):
    """Tracks user login sessions"""
    meta = {'collection': 'user_sessions'}
    
    user_id = ReferenceField(User, required=True)
    login_time = DateTimeField(default=datetime.utcnow)
    logout_time = DateTimeField()
    device_info = StringField(max_length=255)
    ip_address = StringField(max_length=50)
    is_active = BooleanField(default=True)
    # New field to store generated session identifier
    session_id = StringField(max_length=255, required=True)


class Schedule(Document):
    """Learning schedule/commitments"""
    meta = {'collection': 'schedules'}
    
    user_id = ReferenceField(User, required=True)
    title = StringField(max_length=200, required=True)
    description = StringField()
    start_time = DateTimeField(required=True)
    end_time = DateTimeField()
    repeat_pattern = StringField(max_length=50) # weekly, daily, etc.
    is_completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'repeat_pattern': self.repeat_pattern,
            'is_completed': self.is_completed
        }


class Achievement(Document):
    """Predefined achievements/badges"""
    meta = {'collection': 'achievements'}
    
    code = StringField(max_length=50, required=True, unique=True)
    title = StringField(max_length=100, required=True)
    description = StringField(max_length=255)
    xp_reward = IntField(default=0)
    icon = StringField(max_length=100)
    
    def to_dict(self):
        return {
            'code': self.code,
            'title': self.title,
            'description': self.description,
            'xp_reward': self.xp_reward,
            'icon': self.icon
        }

class UserAchievement(Document):
    """Records which users have earned which achievements"""
    meta = {'collection': 'user_achievements'}
    
    user_id = ReferenceField(User, required=True)
    achievement_code = StringField(required=True)
    earned_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'achievement_code': self.achievement_code,
            'earned_at': self.earned_at.isoformat()
        }


# ============================================================================
# FEATURE 1: UNIFIED LEARNING INBOX MODELS
# ============================================================================

class LearningItem(Document):
    """Unified model for all learning content types in the inbox"""
    meta = {'collection': 'learning_items'}
    
    user_id = ReferenceField(User, required=True)
    title = StringField(max_length=300, required=True)
    description = StringField()
    
    # Source Information
    source_type = StringField(max_length=50, required=True)  # course, video, pdf, bookmark, playlist, article
    source_url = StringField(max_length=500)
    platform = StringField(max_length=100)  # udemy, youtube, coursera, local, medium, etc.
    
    # Status Management
    status = StringField(max_length=20, default='active')  # active, paused, completed, dropped
    
    # Duration Tracking
    total_duration = IntField(default=0)  # in minutes
    completed_duration = IntField(default=0)  # in minutes
    
    # Content Metadata (flexible JSON storage)
    metadata = DictField()  # chapters, videos, pages, sections, etc.
    
    # Timestamps
    added_at = DateTimeField(default=datetime.utcnow)
    started_at = DateTimeField()
    completed_at = DateTimeField()
    paused_at = DateTimeField()
    
    # Priority and Scheduling
    priority_score = FloatField(default=0.0)
    target_completion_date = DateTimeField()
    
    # Progress Tracking
    progress_percentage = FloatField(default=0.0)
    last_accessed_at = DateTimeField()
    
    # Tags and Categories
    tags = ListField(StringField(max_length=50))
    category = StringField(max_length=100)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'title': self.title,
            'description': self.description,
            'source_type': self.source_type,
            'source_url': self.source_url,
            'platform': self.platform,
            'status': self.status,
            'total_duration': self.total_duration,
            'completed_duration': self.completed_duration,
            'metadata': self.metadata,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'paused_at': self.paused_at.isoformat() if self.paused_at else None,
            'priority_score': self.priority_score,
            'target_completion_date': self.target_completion_date.isoformat() if self.target_completion_date else None,
            'progress_percentage': self.progress_percentage,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'tags': self.tags,
            'category': self.category
        }
    
    def update_progress(self):
        """Calculate and update progress percentage"""
        if self.total_duration > 0:
            self.progress_percentage = (self.completed_duration / self.total_duration) * 100
        else:
            self.progress_percentage = 0.0
        self.save()


class ContentSource(Document):
    """Tracks external platform integrations for content import"""
    meta = {'collection': 'content_sources'}
    
    user_id = ReferenceField(User, required=True)
    platform_name = StringField(max_length=100, required=True)  # youtube, udemy, coursera, drive, dropbox
    platform_type = StringField(max_length=50, required=True)  # video, course, storage, bookmark
    
    # Authentication/Connection
    is_connected = BooleanField(default=False)
    access_token = StringField(max_length=500)  # encrypted token
    refresh_token = StringField(max_length=500)  # encrypted token
    token_expires_at = DateTimeField()
    
    # Sync Settings
    auto_sync = BooleanField(default=False)
    last_synced_at = DateTimeField()
    sync_frequency = StringField(max_length=20, default='manual')  # manual, daily, weekly
    
    # Import Statistics
    total_items_imported = IntField(default=0)
    last_import_count = IntField(default=0)
    
    # Connection Metadata
    connected_at = DateTimeField(default=datetime.utcnow)
    connection_metadata = DictField()  # platform-specific data
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'platform_name': self.platform_name,
            'platform_type': self.platform_type,
            'is_connected': self.is_connected,
            'auto_sync': self.auto_sync,
            'last_synced_at': self.last_synced_at.isoformat() if self.last_synced_at else None,
            'sync_frequency': self.sync_frequency,
            'total_items_imported': self.total_items_imported,
            'last_import_count': self.last_import_count,
            'connected_at': self.connected_at.isoformat() if self.connected_at else None
        }


# ============================================================================
# FEATURE 2: AUTO COURSE BREAKDOWN INTO DAILY TASKS
# ============================================================================

class LearningPlan(Document):
    """Overall learning plan for a learning item"""
    meta = {'collection': 'learning_plans'}
    
    learning_item_id = ReferenceField(LearningItem, required=True)
    user_id = ReferenceField(User, required=True)
    
    # Plan Configuration
    target_completion_date = DateTimeField(required=True)
    daily_availability_minutes = IntField(required=True)  # How many minutes per day user can study
    total_estimated_duration = IntField(required=True)  # Total course duration in minutes
    
    # Schedule Settings
    skip_weekends = BooleanField(default=True)
    buffer_percentage = FloatField(default=20.0)  # Add 20% buffer time
    
    # Plan Status
    status = StringField(max_length=20, default='active')  # active, completed, abandoned
    created_at = DateTimeField(default=datetime.utcnow)
    last_adjusted_at = DateTimeField()
    
    # Progress Tracking
    total_tasks = IntField(default=0)
    completed_tasks = IntField(default=0)
    missed_tasks = IntField(default=0)
    
    # Metadata
    plan_metadata = DictField()  # Store algorithm parameters, adjustments history
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'learning_item_id': str(self.learning_item_id.id),
            'user_id': str(self.user_id.id),
            'target_completion_date': self.target_completion_date.isoformat() if self.target_completion_date else None,
            'daily_availability_minutes': self.daily_availability_minutes,
            'total_estimated_duration': self.total_estimated_duration,
            'skip_weekends': self.skip_weekends,
            'buffer_percentage': self.buffer_percentage,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'missed_tasks': self.missed_tasks,
            'progress_percentage': (self.completed_tasks / self.total_tasks * 100) if self.total_tasks > 0 else 0
        }


class DailyTask(Document):
    """Individual daily task generated from a learning plan"""
    meta = {'collection': 'daily_tasks'}
    
    learning_plan_id = ReferenceField(LearningPlan, required=True)
    learning_item_id = ReferenceField(LearningItem, required=True)
    user_id = ReferenceField(User, required=True)
    
    # Task Details
    title = StringField(max_length=300, required=True)
    description = StringField()
    task_type = StringField(max_length=50, default='study')  # study, practice, review, project
    
    # Scheduling
    scheduled_date = DateTimeField(required=True)
    estimated_duration_minutes = IntField(required=True)
    
    # Content Reference
    content_reference = DictField()  # chapter, video, page numbers, etc.
    
    # Task Dependencies
    depends_on_task_ids = ListField(StringField())  # IDs of tasks that must be completed first
    is_prerequisite_for = ListField(StringField())  # IDs of tasks that depend on this one
    
    # Difficulty & Priority
    difficulty_level = StringField(max_length=20, default='medium')  # easy, medium, hard
    priority_score = FloatField(default=0.0)
    
    # Status & Progress
    status = StringField(max_length=20, default='pending')  # pending, in_progress, completed, skipped, missed
    completed_at = DateTimeField()
    actual_duration_minutes = IntField(default=0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    started_at = DateTimeField()
    
    # Metadata
    task_metadata = DictField()  # Additional task-specific data
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'learning_plan_id': str(self.learning_plan_id.id),
            'learning_item_id': str(self.learning_item_id.id),
            'user_id': str(self.user_id.id),
            'title': self.title,
            'description': self.description,
            'task_type': self.task_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'estimated_duration_minutes': self.estimated_duration_minutes,
            'content_reference': self.content_reference,
            'depends_on_task_ids': self.depends_on_task_ids,
            'difficulty_level': self.difficulty_level,
            'priority_score': self.priority_score,
            'status': self.status,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'actual_duration_minutes': self.actual_duration_minutes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_overdue': self.is_overdue(),
            'is_today': self.is_today()
        }
    
    def is_overdue(self):
        """Check if task is overdue"""
        if self.status in ['completed', 'skipped']:
            return False
        if self.scheduled_date:
            return datetime.utcnow() > self.scheduled_date
        return False
    
    def is_today(self):
        """Check if task is scheduled for today"""
        if self.scheduled_date:
            today = datetime.utcnow().date()
            task_date = self.scheduled_date.date()
            return today == task_date
        return False
    
    def mark_complete(self, actual_duration=None):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if actual_duration:
            self.actual_duration_minutes = actual_duration
        self.save()
        
        # Update learning plan stats
        plan = self.learning_plan_id
        plan.completed_tasks += 1
        plan.save()


# ============================================================================
# FEATURE 3: HARD COMMITMENT MODE (DISCIPLINE ENFORCEMENT)
# ============================================================================

class Commitment(Document):
    """Locked commitment/promise for a learning item"""
    meta = {'collection': 'commitments'}
    
    learning_item_id = ReferenceField(LearningItem, required=True)
    user_id = ReferenceField(User, required=True)
    
    # Commitment Details
    target_completion_date = DateTimeField(required=True)
    daily_study_minutes = IntField(required=True)  # Committed daily study time
    study_days_per_week = IntField(default=5)  # How many days per week
    
    # Lock Settings
    is_locked = BooleanField(default=True)  # Once locked, cannot be easily modified
    locked_at = DateTimeField()
    modification_count = IntField(default=0)  # Track how many times modified
    max_modifications = IntField(default=2)  # Maximum allowed modifications
    
    # Status
    status = StringField(max_length=20, default='active')  # active, completed, broken, cancelled
    created_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField()
    broken_at = DateTimeField()
    
    # Streak Tracking
    current_streak = IntField(default=0)  # Consecutive days of completion
    longest_streak = IntField(default=0)
    last_check_in = DateTimeField()
    
    # Accountability
    has_accountability_partner = BooleanField(default=False)
    accountability_partner_email = StringField()
    
    # Metadata
    commitment_metadata = DictField()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'learning_item_id': str(self.learning_item_id.id),
            'user_id': str(self.user_id.id),
            'target_completion_date': self.target_completion_date.isoformat() if self.target_completion_date else None,
            'daily_study_minutes': self.daily_study_minutes,
            'study_days_per_week': self.study_days_per_week,
            'is_locked': self.is_locked,
            'modification_count': self.modification_count,
            'max_modifications': self.max_modifications,
            'status': self.status,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_check_in': self.last_check_in.isoformat() if self.last_check_in else None,
            'has_accountability_partner': self.has_accountability_partner,
            'can_modify': self.modification_count < self.max_modifications
        }
    
    def lock(self):
        """Lock the commitment"""
        self.is_locked = True
        self.locked_at = datetime.utcnow()
        self.save()


class CommitmentViolation(Document):
    """Tracks broken commitments and violations"""
    meta = {'collection': 'commitment_violations'}
    
    commitment_id = ReferenceField(Commitment, required=True)
    user_id = ReferenceField(User, required=True)
    
    # Violation Details
    violation_type = StringField(max_length=50, required=True)  # missed_session, late_start, incomplete_duration
    violation_date = DateTimeField(default=datetime.utcnow)
    
    # Severity
    severity_level = IntField(default=1)  # 1-5 (1=warning, 5=critical)
    
    # Consequence Applied
    consequence_applied = StringField(max_length=100)  # warning, streak_reset, content_lockout, etc.
    consequence_duration_hours = IntField(default=0)
    
    # Grace Period
    is_grace_period = BooleanField(default=False)  # First violation gets grace
    
    # Resolution
    is_resolved = BooleanField(default=False)
    resolved_at = DateTimeField()
    resolution_note = StringField()
    
    # Metadata
    violation_metadata = DictField()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'commitment_id': str(self.commitment_id.id),
            'user_id': str(self.user_id.id),
            'violation_type': self.violation_type,
            'violation_date': self.violation_date.isoformat() if self.violation_date else None,
            'severity_level': self.severity_level,
            'consequence_applied': self.consequence_applied,
            'consequence_duration_hours': self.consequence_duration_hours,
            'is_grace_period': self.is_grace_period,
            'is_resolved': self.is_resolved
        }


class AccountabilityPartner(Document):
    """Optional peer accountability system"""
    meta = {'collection': 'accountability_partners'}
    
    user_id = ReferenceField(User, required=True)
    partner_email = StringField(required=True)
    partner_name = StringField()
    
    # Status
    status = StringField(max_length=20, default='pending')  # pending, active, inactive
    invited_at = DateTimeField(default=datetime.utcnow)
    accepted_at = DateTimeField()
    
    # Notification Settings
    notify_on_violations = BooleanField(default=True)
    notify_on_milestones = BooleanField(default=True)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'partner_email': self.partner_email,
            'partner_name': self.partner_name,
            'status': self.status,
            'invited_at': self.invited_at.isoformat() if self.invited_at else None,
            'notify_on_violations': self.notify_on_violations
        }


# ============================================================================
# FEATURE 5: SINGLE FOCUS LEARNING MODE
# ============================================================================

class FocusSession(Document):
    """Tracks active focus mode sessions"""
    meta = {'collection': 'focus_sessions'}
    
    user_id = ReferenceField(User, required=True)
    learning_item_id = ReferenceField(LearningItem, required=True)
    daily_task_id = ReferenceField(DailyTask)  # Optional - specific task being focused on
    
    # Session Details
    started_at = DateTimeField(default=datetime.utcnow)
    ended_at = DateTimeField()
    duration_minutes = IntField(default=0)
    
    # Status
    is_active = BooleanField(default=True)
    exit_reason = StringField(max_length=100)  # completed, emergency_exit, timeout
    
    # Distraction Tracking
    distraction_attempts = IntField(default=0)  # How many times user tried to navigate away
    distraction_log = ListField(DictField())  # Log of distraction attempts
    
    # Progress During Session
    tasks_completed = IntField(default=0)
    content_consumed_minutes = IntField(default=0)
    
    # Session Metadata
    session_metadata = DictField()
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'learning_item_id': str(self.learning_item_id.id),
            'daily_task_id': str(self.daily_task_id.id) if self.daily_task_id else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'duration_minutes': self.duration_minutes,
            'is_active': self.is_active,
            'exit_reason': self.exit_reason,
            'distraction_attempts': self.distraction_attempts,
            'tasks_completed': self.tasks_completed,
            'content_consumed_minutes': self.content_consumed_minutes
        }
    
    def end_session(self, reason='completed'):
        """End the focus session"""
        self.is_active = False
        self.ended_at = datetime.utcnow()
        self.exit_reason = reason
        
        if self.started_at:
            duration = (self.ended_at - self.started_at).total_seconds() / 60
            self.duration_minutes = int(duration)
        
        self.save()
    
    def log_distraction(self, distraction_type, details=None):
        """Log a distraction attempt"""
        self.distraction_attempts += 1
        self.distraction_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'type': distraction_type,
            'details': details or {}
        })
        self.save()

