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
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Onboarding / Learning Context
    learning_goal = StringField(max_length=50) # upskill, switch, academic, hobby
    interests = ListField(StringField(max_length=50)) # tech, business, design, etc.
    commitment_level = StringField(max_length=20) # light, moderate, intensive
    expertise_level = StringField(max_length=20) # beginner, intermediate, advanced

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

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'learning_goal': self.learning_goal,
            'interests': self.interests,
            'commitment_level': self.commitment_level,
            'expertise_level': self.expertise_level,
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
            'high_contrast': self.high_contrast
        }


class OTP(Document):
    """OTP model for verification"""
    meta = {'collection': 'otps'}
    
    email = StringField(max_length=120)
    mobile = StringField(max_length=15)
    otp_code = StringField(max_length=6, required=True)
    otp_type = StringField(max_length=20, required=True) # email_verification, mobile_verification, password_reset
    created_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField(required=True)
    is_used = BooleanField(default=False)
    attempts = IntField(default=0)


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
    relevance_score = FloatField(default=0.0) # AI-calculated relevance
    added_at = DateTimeField(default=datetime.utcnow)
    tags = ListField(StringField(max_length=50))

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'category': self.category,
            'relevance_score': self.relevance_score,
            'added_at': self.added_at.isoformat(),
            'tags': self.tags
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
