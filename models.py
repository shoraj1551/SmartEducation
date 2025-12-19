"""
Database models for SmartEducation
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(15), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # otps relationship removed because OTP.user_id is a String (for temp IDs) and has no foreign key

    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }


class OTP(db.Model):
    """OTP model for verification"""
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)  # Changed to String to support temp user IDs
    otp_code = db.Column(db.String(6), nullable=False)
    otp_type = db.Column(db.String(10), nullable=False)  # 'email' or 'mobile'
    purpose = db.Column(db.String(20), nullable=False)  # 'registration' or 'reset'
    attempts = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_used = db.Column(db.Boolean, default=False)
    
    def is_expired(self):
        """Check if OTP is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_expired() and not self.is_used and self.attempts < 3

class Activity(db.Model):
    """Activity model for tracking user actions"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'course_start', 'survey_complete', etc.
    description = db.Column(db.String(255))
    metadata_json = db.Column(db.Text)  # Additional data in JSON format
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('activities', lazy=True))
    
    def to_dict(self):
        """Convert activity to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'metadata': self.metadata_json,
            'created_at': self.created_at.isoformat()
        }

class Bookmark(db.Model):
    """Bookmark model for tracking educational resources"""
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_educational = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))  # 'video', 'article', 'course', etc.
    tags = db.Column(db.String(255))
    relevance_score = db.Column(db.Float, default=0.0)  # Calculated based on user goals
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('bookmarks', lazy=True))
    
    def to_dict(self):
        """Convert bookmark to dictionary"""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'is_educational': self.is_educational,
            'category': self.category,
            'tags': self.tags,
            'relevance_score': self.relevance_score,
            'created_at': self.created_at.isoformat()
        }
