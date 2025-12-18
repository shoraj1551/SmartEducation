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
        """Register a new user - stores temporarily until OTP verification"""
        from flask import session
        from werkzeug.security import generate_password_hash
        import secrets
        
        # Check if verified user already exists
        existing_user = User.query.filter_by(email=email, is_verified=True).first()
        if existing_user:
            return None, "Email already registered"
        
        existing_mobile = User.query.filter_by(mobile=mobile, is_verified=True).first()
        if existing_mobile:
            return None, "Mobile number already registered"
        
        # Generate temporary user ID
        temp_user_id = secrets.token_hex(16)
        
        # Store user data in session temporarily
        session['pending_user'] = {
            'id': temp_user_id,
            'name': name,
            'email': email,
            'mobile': mobile,
            'password_hash': generate_password_hash(password)
        }
        
        # Generate and send OTPs using temp_user_id
        email_otp = OTPService.create_otp(temp_user_id, 'email', 'registration')
        mobile_otp = OTPService.create_otp(temp_user_id, 'mobile', 'registration')
        
        OTPService.send_email_otp(email, email_otp.otp_code, 'registration')
        OTPService.send_sms_otp(mobile, mobile_otp.otp_code, 'registration')
        
        # Return temp user data
        class TempUser:
            def __init__(self, user_id, email, mobile):
                self.id = user_id
                self.email = email
                self.mobile = mobile
        
        return TempUser(temp_user_id, email, mobile), "Please verify OTP sent to email and mobile."
    
    @staticmethod
    def verify_user(user_id, email_otp, mobile_otp):
        """Verify user with both email and mobile OTP and create account"""
        from flask import session
        
        # Get pending user data from session
        pending_user = session.get('pending_user')
        if not pending_user or pending_user['id'] != user_id:
            return False, "Invalid session or user data not found"
        
        # Verify email OTP
        email_valid, email_msg = OTPService.verify_otp(user_id, email_otp, 'email', 'registration')
        if not email_valid:
            return False, f"Email OTP error: {email_msg}"
        
        # Verify mobile OTP
        mobile_valid, mobile_msg = OTPService.verify_otp(user_id, mobile_otp, 'mobile', 'registration')
        if not mobile_valid:
            return False, f"Mobile OTP error: {mobile_msg}"
        
        # Both OTPs verified - now create the actual user in database
        user = User(
            name=pending_user['name'],
            email=pending_user['email'],
            mobile=pending_user['mobile'],
            is_verified=True  # Mark as verified immediately
        )
        user.password_hash = pending_user['password_hash']  # Set pre-hashed password
        
        db.session.add(user)
        db.session.commit()
        
        # Clear pending user from session
        session.pop('pending_user', None)
        
        # Delete OTP records for temp user
        OTPService.delete_user_otps(user_id)
        
        return True, "User verified and registered successfully"
    
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
