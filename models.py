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
    
    # Advanced Settings (for future expansion)
    extra_settings = DictField()
    
    # Gamification
    xp_total = IntField(default=0)
    level = IntField(default=1)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'is_verified': self.is_verified,
            'job_title': self.job_title,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'education_info': self.education_info,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'website_url': self.website_url,
            'learning_goal': self.learning_goal,
            'interests': self.interests,
            'commitment_level': self.commitment_level,
            'expertise_level': self.expertise_level,
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
            'level': self.level,
            'created_at': self.created_at.isoformat()
        }


class OTP(Document):
    """OTP model for verification"""
    meta = {'collection': 'otps'}
    
    user_id = StringField(max_length=100, required=True)
    otp_code = StringField(max_length=6, required=True)
    otp_type = StringField(max_length=10, required=True)
    purpose = StringField(max_length=20, required=True)
    attempts = IntField(default=0)
    expires_at = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    is_used = BooleanField(default=False)
    
    def is_expired(self):
        """Check if OTP is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_expired() and not self.is_used and self.attempts < 3


class Activity(Document):
    """Activity model for tracking user actions"""
    meta = {'collection': 'activities'}
    
    user_id = ReferenceField(User, required=True)
    activity_type = StringField(max_length=50, required=True)
    description = StringField(max_length=255)
    metadata_json = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert activity to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'activity_type': self.activity_type,
            'description': self.description,
            'metadata': self.metadata_json,
            'created_at': self.created_at.isoformat()
        }


class Bookmark(Document):
    """Bookmark model for tracking educational resources"""
    meta = {'collection': 'bookmarks'}
    
    user_id = ReferenceField(User, required=True)
    url = StringField(max_length=500, required=True)
    title = StringField(max_length=255)
    description = StringField()
    is_educational = BooleanField(default=False)
    category = StringField(max_length=50)
    tags = StringField(max_length=255)
    relevance_score = FloatField(default=0.0)
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert bookmark to dictionary"""
        return {
            'id': str(self.id),
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'is_educational': self.is_educational,
            'category': self.category,
            'tags': self.tags,
            'relevance_score': self.relevance_score,
            'created_at': self.created_at.isoformat()
        }


class UserSession(Document):
    """Session model for tracking user logins and activity periods"""
    meta = {'collection': 'user_sessions'}
    
    user_id = ReferenceField(User, required=True)
    session_id = StringField(max_length=100, required=True, unique=True)
    device_info = DictField()
    ip_address = StringField(max_length=45)
    started_at = DateTimeField(default=datetime.utcnow)
    ended_at = DateTimeField()
    is_active = BooleanField(default=True)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'session_id': self.session_id,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_active': self.is_active,
            'device_info': self.device_info
        }


class Schedule(Document):
    """Schedule model for tracking user learning commitments and tasks"""
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
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'repeat_pattern': self.repeat_pattern,
            'is_completed': self.is_completed
        }

class Achievement(Document):
    """Global milestones available for users to earn"""
    meta = {'collection': 'achievements'}
    
    code = StringField(unique=True, required=True) # e.g. 'first_bookmark'
    title = StringField(required=True)
    description = StringField()
    xp_reward = IntField(default=10)
    icon = StringField() # FontAwesome icon class
    
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
