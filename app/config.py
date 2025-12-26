"""
Configuration settings for SmartEducation application
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Application
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    db_url = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/SmartEducation')
    # MongoDB Settings for Flask-MongoEngine
    MONGODB_SETTINGS = {
        'host': db_url
    }
    # No longer needed for Mongo
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Configuration (Mailtrap for development)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 2525))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@smarteducation.com')
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    # OTP Configuration
    OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES', 10))
    OTP_MAX_ATTEMPTS = int(os.getenv('OTP_MAX_ATTEMPTS', 3))
    OTP_RATE_LIMIT_SECONDS = int(os.getenv('OTP_RATE_LIMIT_SECONDS', 60))
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    @classmethod
    def validate(cls):
        """Validate that required environment variables are set in production."""
        if cls.DEBUG:
            return  # Skip validation in debug mode
        required = {
            'SECRET_KEY': cls.SECRET_KEY,
            'JWT_SECRET_KEY': cls.JWT_SECRET_KEY,
            'MAIL_USERNAME': cls.MAIL_USERNAME,
            'MAIL_PASSWORD': cls.MAIL_PASSWORD,
            'TWILIO_ACCOUNT_SID': cls.TWILIO_ACCOUNT_SID,
            'TWILIO_AUTH_TOKEN': cls.TWILIO_AUTH_TOKEN,
            'TWILIO_PHONE_NUMBER': cls.TWILIO_PHONE_NUMBER,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            # In development or when optional services are not configured, we log a warning instead of raising
            print(f"Warning: Missing environment variables for production: {', '.join(missing)}")

# Run validation when the module is imported (in production mode)
Config.validate()
