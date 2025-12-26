from flask import Blueprint, request, jsonify, g
from functools import wraps
from app.services.security_service import SecurityService
from app.services.auth_service import AuthService
from app.models import User

security_bp = Blueprint('security_bp', __name__, url_prefix='/api/security')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization header is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
            
        # Get full payload to extract session_id
        payload = AuthService.get_token_payload(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
            
        user_id = payload.get('user_id')
        session_id = payload.get('sid')
        
        # Determine if ObjectId or string
        from bson import ObjectId
        uid = ObjectId(user_id) if isinstance(user_id, str) else user_id
        
        user = User.objects(id=uid).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401
            
        g.user = user
        g.session_id = session_id
        return f(*args, **kwargs)
    return decorated

@security_bp.route('/sessions', methods=['GET'])
@login_required
def get_sessions():
    """Get active sessions"""
    try:
        sessions = SecurityService.get_active_sessions(g.user.id, getattr(g, 'session_id', None))
        return jsonify(sessions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_bp.route('/sessions/revoke', methods=['POST'])
@login_required
def revoke_session():
    """Revoke a session"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'error': 'Session ID required'}), 400

    success = SecurityService.revoke_session(g.user.id, session_id)
    if success:
        return jsonify({'message': 'Session revoked'}), 200
    return jsonify({'error': 'Session not found'}), 404

@security_bp.route('/logs', methods=['GET'])
@login_required
def get_logs():
    """Get security activity logs"""
    limit = int(request.args.get('limit', 10))
    logs = SecurityService.get_security_logs(g.user.id, limit)
    return jsonify(logs), 200

@security_bp.route('/2fa/toggle', methods=['POST'])
@login_required
def toggle_2fa():
    """Toggle 2FA"""
    data = request.get_json()
    enable = data.get('enable')
    
    success = SecurityService.toggle_2fa(g.user.id, enable)
    return jsonify({'message': f"2FA {'enabled' if enable else 'disabled'}"}), 200

@security_bp.route('/account/delete-otp', methods=['POST'])
@login_required
def request_delete_otp():
    """Request OTP for account deletion"""
    # Reuse AuthService to send OTP
    try:
        AuthService.send_otp(g.user.email, 'account_deletion')
        return jsonify({'message': 'OTP sent to email'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_bp.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
    """Delete account (requires OTP)"""
    data = request.get_json()
    otp_code = data.get('otp_code')
    
    if not otp_code:
        return jsonify({'error': 'OTP required'}), 400
    
    try:
        SecurityService.delete_account(g.user.id, otp_code)
        return jsonify({'message': 'Account deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

@security_bp.route('/password/update', methods=['POST'])
@login_required
def update_password():
    """Update password with OTP verification"""
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    otp_code = data.get('otp_code')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Current and new passwords are required'}), 400
        
    # 1. Validate Current Password First (to prevent OTP spam/enumeration)
    if not g.user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
        
    # 2. Check for OTP
    if not otp_code:
        # Generate & Send OTP
        try:
            SecurityService.send_action_otp(g.user.id, 'password_change')
            return jsonify({
                'status': 'OTP_REQUIRED', 
                'message': 'For your security, please enter the verification code sent to your email/mobile.'
            }), 200
        except Exception as e:
            return jsonify({'error': 'Failed to send verification code'}), 500
            
    # 3. Verify OTP
    # We check both email and mobile types since we sent to both potentially
    email_valid, _ = AuthService.verify_inline_otp(None, 'email', otp_code, 'password_change') # user_id is implicit in verify_inline_otp context? No.
    # verify_inline_otp uses session['pending_user']. Here users are logged in.
    # We should use OTPService directly or a new helper.
    # Let's look at SecurityService.delete_account which used OTP model directly.
    # We will use that pattern or add verify_otp to SecurityService.
    
    # Better: Use a helper in SecurityService
    try:
        SecurityService.verify_action_otp(g.user.id, otp_code, 'password_change')
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    # 4. Perform Update
    try:
        SecurityService.update_password(g.user.id, current_password, new_password)
        return jsonify({'status': 'SUCCESS', 'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
