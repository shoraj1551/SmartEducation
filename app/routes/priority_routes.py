
"""
Priority Routes (Feature 2)
API endpoints for accessing and managing priority scores.
"""
from flask import Blueprint, request, jsonify
from app.services.priority_service import PriorityService
from app.services.auth_service import AuthService
from functools import wraps

priority_bp = Blueprint('priority', __name__, url_prefix='/api/priority')

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
            
            user_id = AuthService.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
            
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated

@priority_bp.route('/top', methods=['GET'])
@token_required
def get_top_priorities(user_id):
    """Get Top 3 Priority Items"""
    try:
        limit = int(request.args.get('limit', 3))
        items = PriorityService.get_top_priorities(user_id, limit)
        return jsonify({
            'items': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch top priorities: {str(e)}'}), 500

@priority_bp.route('/recalculate', methods=['POST'])
@token_required
def recalculate_priorities(user_id):
    """Force recalculation of all item priorities"""
    try:
        count = PriorityService.recalculate_for_user(user_id)
        return jsonify({
            'message': 'Priorities recalculated successfully',
            'updated_count': count
        }), 200
    except Exception as e:
        return jsonify({'error': f'Recalculation failed: {str(e)}'}), 500
