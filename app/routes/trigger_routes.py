
"""
Trigger & Notification Routes (Feature 11)
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.trigger_service import TriggerService
from functools import wraps

trigger_bp = Blueprint('trigger', __name__, url_prefix='/api')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token: return jsonify({'error': 'Token missing'}), 401
        try:
            if token.startswith('Bearer '): token = token[7:]
            user_id = AuthService.verify_token(token)
            if not user_id: return jsonify({'error': 'Invalid token'}), 401
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except: return jsonify({'error': 'Token error'}), 401
    return decorated

@trigger_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications(user_id):
    """Get active notifications"""
    try:
        # Trigger a check first to ensure fresh data
        TriggerService.evaluate_context(user_id)
        
        notifs = TriggerService.get_notifications(user_id)
        return jsonify([n.to_dict() for n in notifs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trigger_bp.route('/notifications/<n_id>/read', methods=['POST'])
@token_required
def mark_read(user_id, n_id):
    """Mark notification as read"""
    try:
        TriggerService.mark_read(n_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trigger_bp.route('/triggers/check', methods=['POST'])
@token_required
def force_check(user_id):
    """Force context evaluation"""
    try:
        logs = TriggerService.evaluate_context(user_id)
        return jsonify({'logs': logs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
