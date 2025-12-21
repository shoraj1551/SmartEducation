
"""
Reality Checks Routes (Feature 6: The Truth)
API endpoints for accessing strict reality metrics.
"""
from flask import Blueprint, jsonify, request
from app.services.reality_service import RealityService
from app.services.auth_service import AuthService
from functools import wraps

reality_bp = Blueprint('reality', __name__, url_prefix='/api/reality')

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

@reality_bp.route('/metrics', methods=['GET'])
@token_required
def get_truth_metrics(user_id):
    """Get The Harsh Truth Metrics"""
    try:
        metrics = RealityService.calculate_truth_metrics(user_id)
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': f'Failed to calculate truth: {str(e)}'}), 500

@reality_bp.route('/check', methods=['POST'])
@token_required
def check_plan(user_id):
    """
    Feasibility Check for a prospective plan.
    Used by Commitment Modal.
    """
    try:
        data = request.get_json()
        item_id = data.get('learning_item_id')
        target_date_str = data.get('target_date')
        daily_minutes = int(data.get('daily_minutes', 0))
        days_per_week = int(data.get('days_per_week', 5))
        
        from datetime import datetime
        target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00'))
        
        result = RealityService.check_feasibility(
            user_id, item_id, target_date, daily_minutes, days_per_week
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
