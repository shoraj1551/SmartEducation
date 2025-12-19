"""
Weekly Review Routes for Feature 8: Weekly Review Assistant
API endpoints for weekly reviews
"""
from flask import Blueprint, request, jsonify
from services.weekly_review_service import WeeklyReviewService
from services.auth_service import AuthService
from functools import wraps

weekly_review_bp = Blueprint('weekly_review', __name__, url_prefix='/api/weekly-review')


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


@weekly_review_bp.route('/current', methods=['GET'])
@token_required
def get_current_review(user_id):
    """Get current week's review"""
    try:
        review = WeeklyReviewService.generate_weekly_review(user_id, week_offset=0)
        
        return jsonify({'review': review}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to generate review: {str(e)}'}), 500


@weekly_review_bp.route('/week/<int:offset>', methods=['GET'])
@token_required
def get_week_review(user_id, offset):
    """Get review for a specific week (0=current, -1=last week, etc.)"""
    try:
        review = WeeklyReviewService.generate_weekly_review(user_id, week_offset=offset)
        
        return jsonify({'review': review}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to generate review: {str(e)}'}), 500


@weekly_review_bp.route('/history', methods=['GET'])
@token_required
def get_review_history(user_id):
    """Get review history for comparison"""
    try:
        weeks = request.args.get('weeks', default=4, type=int)
        history = WeeklyReviewService.get_review_history(user_id, weeks)
        
        return jsonify({'history': history}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500
