"""
Priority Routes for Feature 4: Smart Priority Engine
API endpoints for priority management
"""
from flask import Blueprint, request, jsonify
from services.priority_service import PriorityService
from services.auth_service import AuthService
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
            
            user_data = AuthService.verify_token(token)
            if not user_data:
                return jsonify({'error': 'Invalid token'}), 401
            
            kwargs['user_id'] = user_data['user_id']
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated


@priority_bp.route('/today', methods=['GET'])
@token_required
def get_top_priority(user_id):
    """Get today's top priority item"""
    try:
        # Get user profile from request (optional)
        user_profile = request.args.get('profile')  # Could be JSON string
        
        top_priority = PriorityService.get_top_priority(user_id, user_profile)
        
        if not top_priority:
            return jsonify({'message': 'No active learning items'}), 200
        
        return jsonify(top_priority), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get top priority: {str(e)}'}), 500


@priority_bp.route('/rankings', methods=['GET'])
@token_required
def get_rankings(user_id):
    """Get all items ranked by priority"""
    try:
        user_profile = request.args.get('profile')
        
        ranked_items = PriorityService.get_ranked_items(user_id, user_profile)
        
        # Format response
        items_data = []
        for ranked_item in ranked_items:
            items_data.append({
                'item': ranked_item['item'].to_dict(),
                'priority_score': ranked_item['priority_score'],
                'breakdown': ranked_item['breakdown']
            })
        
        return jsonify({
            'rankings': items_data,
            'count': len(items_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get rankings: {str(e)}'}), 500


@priority_bp.route('/feedback', methods=['POST'])
@token_required
def submit_feedback(user_id):
    """Submit feedback on priority suggestion"""
    try:
        data = request.get_json()
        
        if not data or 'item_id' not in data or 'feedback_type' not in data:
            return jsonify({'error': 'item_id and feedback_type are required'}), 400
        
        result = PriorityService.record_feedback(
            user_id=user_id,
            item_id=data['item_id'],
            feedback_type=data['feedback_type'],
            feedback_data=data.get('feedback_data')
        )
        
        return jsonify(result), 200 if result['success'] else 404
    
    except Exception as e:
        return jsonify({'error': f'Failed to submit feedback: {str(e)}'}), 500
