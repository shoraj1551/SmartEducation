"""
Authentication service for user management
"""
import jwt
from datetime import datetime, timedelta
from flask import current_app
from mongoengine.queryset.visitor import Q
from app.models import User, UserSession
from app.services.otp_service import OTPService

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def send_verification_otp(name, contact, otp_type, purpose):
        """Send OTP for inline verification"""
        from flask import session
        import secrets
        
        # Check if session exists or create new
        if 'pending_user' not in session or 'id' not in session.get('pending_user', {}):
            temp_user_id = secrets.token_hex(12)
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
        user = User.objects(Q(email=pending_user['email']) | Q(mobile=pending_user['mobile'])).first()
            
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
                is_verified=True,
                is_email_verified=pending_user.get('email_verified', False),
                is_mobile_verified=pending_user.get('mobile_verified', False),
                status='ACTIVE'
            )
            user.password_hash = pending_user['password_hash']
        
        user.save()
        
        # Clear session
        session.pop('pending_user', None)
        OTPService.delete_user_otps(pending_user['id'])
        
        return user, "User registered successfully"

    @staticmethod
    def register_user(name, email, mobile, password, temp_user_id=None):
        """Register a new user - creates User record immediately"""
        import bcrypt
        
        # Check if verified user already exists
        if User.objects(email=email, is_verified=True).first():
            return None, "Email already registered"
        
        if User.objects(mobile=mobile, is_verified=True).first():
            return None, "Mobile number already registered"
            
        # Check if unverified user exists - reuse/overwrite
        user = User.objects(Q(email=email) | Q(mobile=mobile)).first()
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if user:
            # Update existing pending user
            user.name = name
            user.email = email
            user.mobile = mobile
            user.password_hash = password_hash
            user.is_verified = False
            user.is_email_verified = False
            user.is_mobile_verified = False
            user.status = 'PENDING_VERIFICATION'
            user.updated_at = datetime.utcnow()
        else:
            # Create new pending user
            user = User(
                name=name,
                email=email,
                mobile=mobile,
                password_hash=password_hash,
                is_verified=False,
                is_email_verified=False,
                is_mobile_verified=False,
                status='PENDING_VERIFICATION'
            )
        
        user.save()
        
        # Generate and send OTPs
        email_otp = OTPService.create_otp(str(user.id), 'email', 'registration')
        OTPService.send_email_otp(email, email_otp.otp_code, 'registration')
            
        mobile_otp = OTPService.create_otp(str(user.id), 'mobile', 'registration')
        OTPService.send_sms_otp(mobile, mobile_otp.otp_code, 'registration')
            
        # Return user object (TempUser adapter not needed anymore as User is real)
        return user, "Please verify OTPs."

    @staticmethod
    def verify_user(user_id, email_otp, mobile_otp):
        """Verify user with both email and mobile OTP and activate account"""
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, "User not found"
            
        # Verify email OTP if provided
        if email_otp:
            email_valid, email_msg = OTPService.verify_otp(user_id, email_otp, 'email', 'registration')
            if email_valid:
                 user.is_email_verified = True
                     
        # Verify mobile OTP if provided
        if mobile_otp:
             mobile_valid, mobile_msg = OTPService.verify_otp(user_id, mobile_otp, 'mobile', 'registration')
             if mobile_valid:
                 user.is_mobile_verified = True
        
        user.save()

        # Check verifications
        if not user.is_email_verified and not user.is_mobile_verified:
            return False, "Please verify at least one channel (Email or Mobile) to continue."
        
        # Activate User
        user.is_verified = True
        user.status = 'ACTIVE'
        user.save()
        
        # Delete OTP records
        OTPService.delete_user_otps(user_id)
        
        return user, "User verified and registered successfully"
    
    @staticmethod
    def login_user(identifier, password, device_info=None, ip_address=None):
        """Login user with email/mobile and password (BUG-007 fix)"""
        # Check if identifier is email or mobile
        # IMPORTANT: Only match verified users to prevent duplicate logins
        user = User.objects(
            Q(email=identifier, is_verified=True) | Q(mobile=identifier, is_verified=True)
        ).first()
        
        if not user:
            return None, "Invalid credentials"
        
        # Verify password
        if not user.check_password(password):
            return None, "Invalid credentials"
        
        # Check verification/status
        # Backward compatibility: If no status but verified, treat as ACTIVE
        current_status = getattr(user, 'status', None)
        if not current_status:
            if user.is_verified:
                current_status = 'ACTIVE'
                # Optional: Self-heal
                user.status = 'ACTIVE'
                user.save()
            else:
                current_status = 'PENDING_VERIFICATION'

        if current_status != 'ACTIVE':
             if not user.is_verified or current_status in ['PENDING_VERIFICATION', 'PARTIAL_VERIFIED']:
                 return {
                     'error_code': 'VERIFICATION_REQUIRED',
                     'user_id': str(user.id),
                     'verified_channels': {
                         'email': user.is_email_verified,
                         'mobile': user.is_mobile_verified
                     }
                 }, "Verification required"
             return None, f"Account status is {current_status}. Please contact support."
        
        # ENFORCEMENT 1: Two-Factor Authentication
        # If enabled, do not create session yet. Send OTP and return requirement.
        if getattr(user, 'is_2fa_enabled', False):
            # Send Login OTP
            otp = OTPService.create_otp(str(user.id), 'email', 'login_2fa')
            OTPService.send_email_otp(user.email, otp.otp_code, 'login verification')
            
            return {
                'error_code': '2FA_REQUIRED',
                'user_id': str(user.id),
                'email': user.email
            }, "Two-Factor Authentication required"

        # ENFORCEMENT 2: Login Alerts
        if getattr(user, 'login_alerts_enabled', False):
            # Send alert asynchronously (or sync for now since simple)
            OTPService.send_email_login_alert(
                user.email,
                device_info or "Unknown Device",
                ip_address or "Unknown IP",
                datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            )
        
        # Create Session ID first
        import secrets
        session_id = secrets.token_hex(16)
        
        # Generate JWT token with session_id
        token = AuthService.generate_token(user.id, session_id)
        
        # Create UserSession
        user_session = UserSession(
            user_id=user,
            session_id=session_id,
            is_active=True,
            device_info=device_info,
            ip_address=ip_address
        )
        user_session.save()
        
        return {
            'user': user.to_dict(), 
            'token': token,
            'session_id': session_id
        }, "Login successful"
    
    @staticmethod
    def request_password_reset(identifier):
        """Request password reset via email or mobile"""
        # Normalize identifier if it looks like email
        if '@' in identifier:
            identifier = identifier.strip().lower()
            # Case insensitive search for email
            user = User.objects(email__iexact=identifier).first()
        else:
            # Assume mobile - strip non-digits for search if needed
            # User might type spaced mobile, DB stores raw digits
            clean_mobile = ''.join(filter(str.isdigit, str(identifier)))
            # Try to find by normalized or raw
            user = User.objects(mobile=clean_mobile).first()
            if not user:
                 user = User.objects(mobile=identifier).first()
        
        if not user:
            return None, "User not found"
        
        # Security: Should we allow reset for unverified users?
        # If they exist but blocked by verification, maybe yes, to let them recover?
        # But we need verified email/mobile to send OTP!
        # If is_email_verified is False, we can't trust the email.
        
        # Generate and send OTPs
        # Only send to verified channels!
        
        sent_any = False
        
        if user.is_email_verified or user.is_verified: # Backward compat
             email_otp = OTPService.create_otp(str(user.id), 'email', 'reset')
             OTPService.send_email_otp(user.email, email_otp.otp_code, 'password reset')
             sent_any = True
             
        if user.is_mobile_verified or user.is_verified:
             mobile_otp = OTPService.create_otp(str(user.id), 'mobile', 'reset')
             OTPService.send_sms_otp(user.mobile, mobile_otp.otp_code, 'password reset')
             sent_any = True
             
        if not sent_any:
            # If nothing verified, maybe send to connection provided?
            # Risky. Let's stick to simple flow for now: Send to both if verified.
            # If user is totally unverified, they should REGISTER again (which now works since we cleaned up).
            return None, "User found but no verified contact channels. Please contact support or register again."
        
        return user, "OTP sent to your verified channels"
    
    @staticmethod
    def reset_password(user_id, email_otp, mobile_otp, new_password):
        """Reset password with OTP verification"""
        user = User.objects(id=user_id).first()
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
        
        # Check password history - new password cannot match last 3 passwords
        if user.check_password_in_history(new_password, count=3):
            return False, "New password cannot match your last 3 passwords. Please choose a different password."
        
        # Save current password to history before updating
        if user.password_hash:
            user.add_to_password_history(user.password_hash)
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        return True, "Password reset successfully"
    
    @staticmethod
    def resend_otp(user_id, otp_type, purpose):
        """Resend OTP"""
        user = User.objects(id=user_id).first()
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
    def generate_token(user_id, session_id=None):
        """Generate JWT token"""
        payload = {
            'user_id': str(user_id),
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }
        if session_id:
            payload['sid'] = session_id
            
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user_id"""
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except Exception:
            return None

    @staticmethod
    def verify_2fa_and_login(user_id, otp_code, device_info=None, ip_address=None):
        """Verify 2FA OTP and complete login"""
        # Verify OTP
        is_valid, message = OTPService.verify_otp(user_id, otp_code, 'email', 'login_2fa')
        
        if not is_valid:
            return None, message
            
        user = User.objects(id=user_id).first()
        if not user:
             return None, "User not found"
             
        # ENFORCEMENT 2: Login Alerts (Triggered here for 2FA users)
        if getattr(user, 'login_alerts_enabled', False):
            OTPService.send_email_login_alert(
                user.email,
                device_info or "Unknown Device",
                ip_address or "Unknown IP",
                datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            )
            
        # Create Session ID
        import secrets
        session_id = secrets.token_hex(16)
        
        # Generate JWT token with session_id
        token = AuthService.generate_token(user.id, session_id)
        
        # Create UserSession
        user_session = UserSession(
            user_id=user,
            session_id=session_id,
            is_active=True,
            device_info=device_info,
            ip_address=ip_address
        )
        user_session.save()
        
        return {
            'user': user.to_dict(), 
            'token': token,
            'session_id': session_id
        }, "Login successful"

    @staticmethod
    def get_token_payload(token):
        """Verify token and return full payload"""
        try:
            return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except Exception:
            return None

class TempUser:
    """Temporary user object for registration flow"""
    def __init__(self, user_id, email, mobile, is_verified):
        self.id = user_id
        self.email = email
        self.mobile = mobile
        self.is_verified = is_verified

