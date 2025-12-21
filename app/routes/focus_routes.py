"""
Focus Mode Routes for Feature 5: Single Focus Learning Mode
API endpoints for focus mode management
"""
from flask import Blueprint, request, jsonify
from app.services.focus_service import FocusModeService
from app.services.auth_service import AuthService
from functools import wraps

focus_bp = Blueprint('focus', __name__, url_prefix='/api/focus')


def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_data = AuthService.verify_token(token)
            if not user_data:
                return jsonify({'error': 'Invalid token'}), 401
            
            kwargs['user_id'] = user_data['user_id']
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated


@focus_bp.route('/activate', methods=['POST'])
@token_required
def activate_focus(user_id):
    """Start focus mode for an item"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        session = FocusModeService.activate_focus_mode(
            user_id=user_id,
            learning_item_id=data['learning_item_id'],
            daily_task_id=data.get('daily_task_id')
        )
        
        return jsonify({
            'message': 'Focus mode activated',
            'session': session.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to activate focus mode: {str(e)}'}), 500


@focus_bp.route('/deactivate', methods=['POST'])
@token_required
def deactivate_focus(user_id):
    """End focus mode"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id')
        reason = data.get('reason', 'completed')
        
        if not session_id:
            # Try to get active session
            active_session = FocusModeService.get_active_session(user_id)
            if not active_session:
                return jsonify({'error': 'No active focus session'}), 404
            session_id = str(active_session.id)
        
        session = FocusModeService.deactivate_focus_mode(session_id, reason)
        
        return jsonify({
            'message': 'Focus mode deactivated',
            'session': session.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to deactivate focus mode: {str(e)}'}), 500


@focus_bp.route('/current', methods=['GET'])
@token_required
def get_current_session(user_id):
    """Get current active focus session"""
    try:
        session = FocusModeService.get_active_session(user_id)
        
        if not session:
            return jsonify({'active': False, 'session': None}), 200
        
        return jsonify({
            'active': True,
            'session': session.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get current session: {str(e)}'}), 500


@focus_bp.route('/stats', methods=['GET'])
@token_required
def get_focus_stats(user_id):
    """Get focus mode analytics"""
    try:
        days = request.args.get('days', default=30, type=int)
        stats = FocusModeService.get_focus_stats(user_id, days)
        
        return jsonify({'stats': stats}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500


@focus_bp.route('/distraction', methods=['POST'])
@token_required
def log_distraction(user_id):
    """Log a distraction attempt"""
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return jsonify({'error': 'session_id is required'}), 400
        
        session = FocusModeService.log_distraction_attempt(
            session_id=data['session_id'],
            distraction_type=data.get('distraction_type', 'navigation'),
            details=data.get('details')
        )
        
        return jsonify({
            'message': 'Distraction logged',
            'distraction_count': session.distraction_attempts
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to log distraction: {str(e)}'}), 500
