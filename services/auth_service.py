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
    def send_verification_otp(name, contact, otp_type, purpose):
        """Send OTP for inline verification"""
        from flask import session
        import secrets
        
        # Check if session exists or create new
        if 'pending_user' not in session or 'id' not in session.get('pending_user', {}):
            temp_user_id = secrets.token_hex(16)
            session['pending_user'] = {
                'id': temp_user_id,
                'name': name,
                'email': contact if otp_type == 'email' else '',
                'mobile': contact if otp_type == 'mobile' else '',
                'email_verified': False,
                'mobile_verified': False,
                'password_hash': None  # Initialize to prevent KeyError
            }
        else:
            temp_user_id = session['pending_user']['id']
            # Update contact info
            if otp_type == 'email':
                session['pending_user']['email'] = contact
            else:
                session['pending_user']['mobile'] = contact
                
        # Generate and send OTP
        otp = OTPService.create_otp(temp_user_id, otp_type, purpose)
        if not otp:
             raise ValueError("Failed to generate OTP")
        
        if otp_type == 'email':
            OTPService.send_email_otp(contact, otp.otp_code, purpose)
        else:
            OTPService.send_sms_otp(contact, otp.otp_code, purpose)
            
        return temp_user_id
        
    @staticmethod
    def verify_inline_otp(temp_user_id, otp_type, otp_code, purpose):
        """Verify inline OTP and update session"""
        from flask import session
        
        # Verify OTP
        is_valid, message = OTPService.verify_otp(temp_user_id, otp_code, otp_type, purpose)
        
        if is_valid:
            # Update session verification status
            if 'pending_user' in session and session['pending_user']['id'] == temp_user_id:
                if otp_type == 'email':
                    session['pending_user']['email_verified'] = True
                else:
                    session['pending_user']['mobile_verified'] = True
                session.modified = True
                return True, "Verified successfully"
            return False, "Session expired"
        return False, message

    @staticmethod
    def create_verified_user_from_session():
        """Create user immediately from verified session data"""
        from flask import session
        
        pending_user = session.get('pending_user')
        if not pending_user:
            return None, "Session expired"
            
        # Check if user already exists (unverified)
        user = User.query.filter_by(email=pending_user['email']).first()
        if not user:
            user = User.query.filter_by(mobile=pending_user['mobile']).first()
            
        if user:
            # Update existing unverified user
            user.name = pending_user['name']
            user.email = pending_user['email']
            user.mobile = pending_user['mobile']
            user.password_hash = pending_user['password_hash']
            user.is_verified = True
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                name=pending_user['name'],
                email=pending_user['email'],
                mobile=pending_user['mobile'],
                is_verified=True
            )
            user.password_hash = pending_user['password_hash']
        
        db.session.add(user)
        db.session.commit()
        
        # Clear session
        session.pop('pending_user', None)
        OTPService.delete_user_otps(pending_user['id'])
        
        return user, "User registered successfully"

    @staticmethod
    def register_user(name, email, mobile, password, temp_user_id=None):
        """Register a new user - checks for existing verification"""
        from flask import session
        import bcrypt
        import secrets
        
        # Check if verified user already exists
        existing_user = User.query.filter_by(email=email, is_verified=True).first()
        if existing_user:
            return None, "Email already registered"
        
        existing_mobile = User.query.filter_by(mobile=mobile, is_verified=True).first()
        if existing_mobile:
            return None, "Mobile number already registered"
            
        # Check if we have a valid pre-verified session
        if temp_user_id and 'pending_user' in session and session['pending_user']['id'] == temp_user_id:
            # Update fields
            session['pending_user']['name'] = name
            session['pending_user']['email'] = email
            session['pending_user']['mobile'] = mobile
            session['pending_user']['password_hash'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Check if ALREADY verified
            if session['pending_user'].get('email_verified') and session['pending_user'].get('mobile_verified'):
                # Immediate creation!
                return AuthService.create_verified_user_from_session()
        
        # Fresh registration or incomplete verification
        if not temp_user_id or 'pending_user' not in session:
            temp_user_id = secrets.token_hex(16)
            session['pending_user'] = {
                'id': temp_user_id,
                'name': name,
                'email': email,
                'mobile': mobile,
                # Use bcrypt here too
                'password_hash': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'email_verified': False,

                'mobile_verified': False
            }
        
        # Generate and send OTPs Only if NOT verified yet
        # If one is verified, skip sending that one
        
        email_verified = session['pending_user'].get('email_verified', False)
        mobile_verified = session['pending_user'].get('mobile_verified', False)
        
        if not email_verified:
            email_otp = OTPService.create_otp(temp_user_id, 'email', 'registration')
            OTPService.send_email_otp(email, email_otp.otp_code, 'registration')
            
        if not mobile_verified:

            mobile_otp = OTPService.create_otp(temp_user_id, 'mobile', 'registration')
            OTPService.send_sms_otp(mobile, mobile_otp.otp_code, 'registration')
            
        # Return temp user data
        is_fully_verified = email_verified and mobile_verified
        return TempUser(temp_user_id, email, mobile, is_fully_verified), "Please verify OTPs."    
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
        
        # Both OTPs verified - now create or update the user in database
        
        # Check if user already exists (unverified)
        user = User.query.filter_by(email=pending_user['email']).first()
        if not user:
            user = User.query.filter_by(mobile=pending_user['mobile']).first()
            
        if user:
            # Update existing unverified user
            user.name = pending_user['name']
            user.email = pending_user['email']
            user.mobile = pending_user['mobile']
            user.password_hash = pending_user['password_hash']
            user.is_verified = True
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                name=pending_user['name'],
                email=pending_user['email'],
                mobile=pending_user['mobile'],
                is_verified=True  # Mark as verified immediately
            )
            user.password_hash = pending_user['password_hash']
        
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

class TempUser:
    """Temporary user object for registration flow"""
    def __init__(self, user_id, email, mobile, is_verified):
        self.id = user_id
        self.email = email
        self.mobile = mobile
        self.is_verified = is_verified

