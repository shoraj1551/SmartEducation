"""
Authentication routes for SmartEducation API
"""
from flask import Blueprint, request, jsonify
from app.models import User
from app.services.auth_service import AuthService
from app.services.activity_service import ActivityService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Mobile Number Validation (IMPROVEMENT-002)
def validate_and_normalize_mobile(mobile):
    """
    Validate and normalize mobile number
    Accepts: 10 digits (without country code) or 12 digits (with country code 91)
    Returns: (is_valid, normalized_mobile, error_message)
    """
    if not mobile:
        return False, None, "Mobile number is required"
    
    # Remove spaces, dashes, plus signs, and other non-digit characters
    mobile_clean = ''.join(filter(str.isdigit, str(mobile)))
    
    # Check length
    if len(mobile_clean) == 10:
        # Without country code - valid
        return True, mobile_clean, None
    elif len(mobile_clean) == 12:
        # With country code - normalize to 10 digits
        if mobile_clean.startswith('91'):
            normalized = mobile_clean[2:]  # Remove country code
            return True, normalized, None
        else:
            return False, None, "Invalid country code. Please use 91 (India) or omit country code."
    else:
        return False, None, f"Mobile number must be 10 digits (e.g., 9876543210) or 12 digits with country code (e.g., 919876543210). Got {len(mobile_clean)} digits."

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'mobile', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Email validation (BUG-008 fix)
        import re
        email = data['email'].strip().lower()
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format. Please use a valid email address.'}), 400
        
        # Block test/temporary email domains
        blocked_domains = [
            'test.com', 'example.com', 'temp.com', 'temporary.com',
            'fake.com', 'dummy.com', 'invalid.com', 'localhost.com'
        ]
        email_domain = email.split('@')[1] if '@' in email else ''
        if email_domain in blocked_domains:
            return jsonify({'error': 'Please use a valid email address. Test/temporary emails are not allowed.'}), 400
        
        # Mobile validation (IMPROVEMENT-002)
        is_valid_mobile, normalized_mobile, mobile_error = validate_and_normalize_mobile(data['mobile'])
        if not is_valid_mobile:
            return jsonify({'error': mobile_error}), 400
        
        # Register user
        user, message = AuthService.register_user(
            data['name'],
            email,  # Use validated/normalized email
            normalized_mobile,  # Use validated/normalized mobile
            data['password'],
            data.get('temp_user_id')  # Pass temp ID if available
        )
        
        if not user:
            return jsonify({'error': message}), 400
            
        # Ensure user object has ID (Robustness Fix)
        if not hasattr(user, 'id'):
             return jsonify({'error': 'Registration failed: User object missing ID'}), 500


        # Check if user is already fully verified (immediate creation)
        if hasattr(user, 'is_verified') and user.is_verified is True:
            # Check if it's a real User model (has created_at) or TempUser
            if hasattr(user, 'created_at'):
                # This is a real user! Registration complete!
                return jsonify({
                    'message': 'Registration successful!',
                    'user_id': str(user.id),
                    'email': user.email,
                    'mobile': user.mobile,
                    'verification_completed': True
                }), 201
        
        return jsonify({
            'message': message,
            'user_id': str(user.id),
            'email': user.email,

            'mobile': user.mobile,
            'verification_completed': False
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/send-verification-otp', methods=['POST'])
def send_verification_otp():
    """Send OTP for inline verification"""
    try:
        data = request.get_json()
        
        if not all([data.get('name')]):
             return jsonify({'error': 'Name is required'}), 400
             
        contact = data.get('email') or data.get('mobile')
        if not contact:
            return jsonify({'error': 'Email or mobile is required'}), 400
        
        otp_type = data.get('otp_type')
        if otp_type not in ['email', 'mobile']:
            return jsonify({'error': 'Invalid OTP type'}), 400

        # Validate and normalize mobile if otp_type is mobile (IMPROVEMENT-002)
        if otp_type == 'mobile':
            is_valid, normalized_mobile, error = validate_and_normalize_mobile(contact)
            if not is_valid:
                return jsonify({'error': error}), 400
            contact = normalized_mobile
            
        temp_user_id = AuthService.send_verification_otp(
            data['name'],
            contact,
            otp_type,
            'registration'
        )
        
        return jsonify({
            'message': 'OTP sent successfully',
            'temp_user_id': temp_user_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@auth_bp.route('/verify-inline-otp', methods=['POST'])
def verify_inline_otp():
    """Verify inline OTP"""
    try:
        data = request.get_json()
        
        required = ['temp_user_id', 'otp_type', 'otp_code']
        if not all([data.get(f) for f in required]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        success, message = AuthService.verify_inline_otp(
            data['temp_user_id'],
            data['otp_type'],
            data['otp_code'],
            'registration'
        )
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        # Validate required fields
        if not data.get('user_id'):
            return jsonify({'error': 'user_id is required'}), 400
        
        if not data.get('email_otp') and not data.get('mobile_otp'):
             return jsonify({'error': 'At least one OTP (email or mobile) is required'}), 400
        
        # Verify OTPs
        user, message = AuthService.verify_user(
            data['user_id'],
            data['email_otp'],
            data['mobile_otp']
        )
        
        if not user:
            return jsonify({'error': message}), 400
        
        # user object is now returned directly from verify_user
        token = AuthService.generate_token(user.id)
        
        return jsonify({
            'message': message,
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all([data.get('user_id'), data.get('otp_type'), data.get('purpose')]):
            return jsonify({'error': 'user_id, otp_type, and purpose are required'}), 400
        
        # Resend OTP
        success, message = AuthService.resend_otp(
            data['user_id'],
            data['otp_type'],
            data['purpose']
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with email/mobile and password"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all([data.get('identifier'), data.get('password')]):
            return jsonify({'error': 'identifier (email/mobile) and password are required'}), 400
        
        identifier = data['identifier'].strip()
        
        # Check if identifier looks like a mobile number (IMPROVEMENT-002)
        # Remove common separators and check if it's all digits
        test_identifier = identifier.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # If identifier is all digits, treat as mobile and normalize
        if test_identifier.isdigit():
            is_valid, normalized_mobile, error = validate_and_normalize_mobile(test_identifier)
            if is_valid:
                identifier = normalized_mobile
                print(f"[LOGIN DEBUG] Mobile normalized: {test_identifier} -> {normalized_mobile}")
            else:
                print(f"[LOGIN DEBUG] Mobile validation failed: {error}")
                # Still try login with original identifier (will fail with invalid credentials)
        else:
            # Treat as email
            identifier = identifier.lower()
            print(f"[LOGIN DEBUG] Email login: {identifier}")
        
        # Login user
        result, message = AuthService.login_user(
            identifier,
            data['password']
        )
        
        if not result:
            return jsonify({'error': message}), 401
            
        # Check for structured verification error (returned as result dict with error_code)
        if isinstance(result, dict) and result.get('error_code') == 'VERIFICATION_REQUIRED':
            return jsonify({
                'code': 'VERIFICATION_REQUIRED',
                'error': message,
                'nextStep': 'OTP_VERIFICATION',
                'userId': result.get('user_id'),
                'verifiedChannels': result.get('verified_channels')
            }), 403
        
        # Log successful login
        ActivityService.log_activity(result['user']['id'], 'login', 'User logged in successfully')
        return jsonify({
            'message': message,
            'user': result['user'],
            'token': result['token']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        
        # Validate required field
        if not data.get('identifier'):
            return jsonify({'error': 'identifier (email/mobile) is required'}), 400
        
        # Request password reset
        user, message = AuthService.request_password_reset(data['identifier'])
        
        if not user:
            return jsonify({'error': message}), 404
        
        return jsonify({
            'message': message,
            'user_id': str(user.id)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with OTP verification"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'email_otp', 'mobile_otp', 'new_password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Reset password
        success, message = AuthService.reset_password(
            data['user_id'],
            data['email_otp'],
            data['mobile_otp'],
            data['new_password']
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        
        if not data.get('token'):
            return jsonify({'error': 'token is required'}), 400
        
        user_id = AuthService.verify_token(data['token'])
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.objects(id=user_id).first()
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
