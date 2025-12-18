"""
Authentication service for user management
"""
import jwt
from datetime import datetime, timedelta
from flask import current_app
from models import db, User
from services.otp_service import OTPService

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register_user(name, email, mobile, password):
        """Register a new user"""
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return None, "Email already registered"
        
        if User.query.filter_by(mobile=mobile).first():
            return None, "Mobile number already registered"
        
        # Create new user
        user = User(
            name=name,
            email=email,
            mobile=mobile,
            is_verified=False
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate and send OTPs
        email_otp = OTPService.create_otp(user.id, 'email', 'registration')
        mobile_otp = OTPService.create_otp(user.id, 'mobile', 'registration')
        
        OTPService.send_email_otp(email, email_otp.otp_code, 'registration')
        OTPService.send_sms_otp(mobile, mobile_otp.otp_code, 'registration')
        
        return user, "User registered successfully. Please verify OTP sent to email and mobile."
    
    @staticmethod
    def verify_user(user_id, email_otp, mobile_otp):
        """Verify user with both email and mobile OTP"""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        # Verify email OTP
        email_valid, email_msg = OTPService.verify_otp(user_id, email_otp, 'email', 'registration')
        if not email_valid:
            return False, f"Email OTP error: {email_msg}"
        
        # Verify mobile OTP
        mobile_valid, mobile_msg = OTPService.verify_otp(user_id, mobile_otp, 'mobile', 'registration')
        if not mobile_valid:
            return False, f"Mobile OTP error: {mobile_msg}"
        
        # Mark user as verified
        user.is_verified = True
        db.session.commit()
        
        return True, "User verified successfully"
    
    @staticmethod
    def login_user(identifier, password):
        """Login user with email/mobile and password"""
        # Check if identifier is email or mobile
        user = User.query.filter(
            (User.email == identifier) | (User.mobile == identifier)
        ).first()
        
        if not user:
            return None, "Invalid credentials"
        
        if not user.check_password(password):
            return None, "Invalid credentials"
        
        if not user.is_verified:
            return None, "Please verify your account first"
        
        # Generate JWT token
        token = AuthService.generate_token(user.id)
        
        return {'user': user.to_dict(), 'token': token}, "Login successful"
    
    @staticmethod
    def request_password_reset(identifier):
        """Request password reset via email or mobile"""
        # Find user by email or mobile
        user = User.query.filter(
            (User.email == identifier) | (User.mobile == identifier)
        ).first()
        
        if not user:
            return None, "User not found"
        
        # Generate and send OTPs
        email_otp = OTPService.create_otp(user.id, 'email', 'reset')
        mobile_otp = OTPService.create_otp(user.id, 'mobile', 'reset')
        
        OTPService.send_email_otp(user.email, email_otp.otp_code, 'password reset')
        OTPService.send_sms_otp(user.mobile, mobile_otp.otp_code, 'password reset')
        
        return user, "OTP sent to your email and mobile"
    
    @staticmethod
    def reset_password(user_id, email_otp, mobile_otp, new_password):
        """Reset password with OTP verification"""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        # Verify email OTP
        email_valid, email_msg = OTPService.verify_otp(user_id, email_otp, 'email', 'reset')
        if not email_valid:
            return False, f"Email OTP error: {email_msg}"
        
        # Verify mobile OTP
        mobile_valid, mobile_msg = OTPService.verify_otp(user_id, mobile_otp, 'mobile', 'reset')
        if not mobile_valid:
            return False, f"Mobile OTP error: {mobile_msg}"
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return True, "Password reset successfully"
    
    @staticmethod
    def resend_otp(user_id, otp_type, purpose):
        """Resend OTP"""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        # Create new OTP
        otp = OTPService.create_otp(user_id, otp_type, purpose)
        
        # Send OTP
        if otp_type == 'email':
            OTPService.send_email_otp(user.email, otp.otp_code, purpose)
        else:
            OTPService.send_sms_otp(user.mobile, otp.otp_code, purpose)
        
        return True, f"OTP resent to {otp_type}"
    
    @staticmethod
    def generate_token(user_id):
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
