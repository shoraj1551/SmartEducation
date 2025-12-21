
"""
Wellness Routes (Feature 8: Burnout & Review)
API endpoints for user sustainability (burnout check, weekly review).
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.burnout_service import BurnoutService
from app.services.review_service import WeeklyReviewService
from functools import wraps

wellness_bp = Blueprint('wellness', __name__, url_prefix='/api/wellness')

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

@wellness_bp.route('/burnout', methods=['GET'])
@token_required
def check_burnout(user_id):
    """Check burnout risk status"""
    try:
        report = BurnoutService.check_burnout_risk(user_id)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wellness_bp.route('/review', methods=['GET'])
@token_required
def get_weekly_review(user_id):
    """Get weekly review summary"""
    try:
        summary = WeeklyReviewService.get_weekly_summary(user_id)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
