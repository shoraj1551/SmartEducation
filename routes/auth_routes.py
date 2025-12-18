"""
Authentication routes for SmartEducation API
"""
from flask import Blueprint, request, jsonify
from models import db, User
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
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
            data['password']
        )
        
        if not user:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message,
            'user_id': user.id,
            'email': user.email,
            'mobile': user.mobile
        }), 201
        
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
        success, message = AuthService.verify_user(
            data['user_id'],
            data['email_otp'],
            data['mobile_otp']
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        # Get user and generate token
        user = User.query.get(data['user_id'])
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
        
        user = User.query.get(user_id)
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
