"""
Authentication routes for SmartEducation API
"""
from flask import Blueprint, request, jsonify
from models import User
from services.auth_service import AuthService
from services.activity_service import ActivityService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

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
        
        # Register user
        user, message = AuthService.register_user(
            data['name'],
            data['email'],
            data['mobile'],
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
                    'user_id': user.id,
                    'email': user.email,
                    'mobile': user.mobile,
                    'verification_completed': True
                }), 201
        
        return jsonify({
            'message': message,
            'user_id': user.id,
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
        if not all([data.get('user_id'), data.get('email_otp'), data.get('mobile_otp')]):
            return jsonify({'error': 'user_id, email_otp, and mobile_otp are required'}), 400
        
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
        
        # Login user
        result, message = AuthService.login_user(
            data['identifier'],
            data['password']
        )
        
        if not result:
            return jsonify({'error': message}), 401
        
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
            'user_id': user.id
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
