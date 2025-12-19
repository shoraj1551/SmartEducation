"""
Database models for SmartEducation (MongoDB)
"""
from datetime import datetime
from mongoengine import (
    Document, StringField, BooleanField, DateTimeField, 
    IntField, ReferenceField, FloatField
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
            'theme_preference': self.theme_preference,
            'email_notifications': self.email_notifications,
            'mobile_notifications': self.mobile_notifications,
            'marketing_emails': self.marketing_emails,
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
