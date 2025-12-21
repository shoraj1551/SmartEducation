"""
Burnout Routes for Feature 9: Burnout-Aware Adaptive Scheduling
API endpoints for burnout detection and adaptive scheduling
"""
from flask import Blueprint, request, jsonify
from app.services.burnout_service import BurnoutDetectionService
from app.services.auth_service import AuthService
from functools import wraps

burnout_bp = Blueprint('burnout', __name__, url_prefix='/api/burnout')


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


@burnout_bp.route('/score', methods=['GET'])
@token_required
def get_burnout_score(user_id):
    """Get burnout score and risk level"""
    try:
        days = request.args.get('days', default=14, type=int)
        score_data = BurnoutDetectionService.calculate_burnout_score(user_id, days)
        
        return jsonify(score_data), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to calculate burnout score: {str(e)}'}), 500


@burnout_bp.route('/recommendations', methods=['GET'])
@token_required
def get_recommendations(user_id):
    """Get adaptive scheduling recommendations"""
    try:
        recommendations = BurnoutDetectionService.get_adaptive_recommendations(user_id)
        
        return jsonify({'recommendations': recommendations}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500


@burnout_bp.route('/adapt-schedule/<plan_id>', methods=['POST'])
@token_required
def adapt_schedule(user_id, plan_id):
    """Apply adaptive scheduling to a learning plan"""
    try:
        plan = BurnoutDetectionService.apply_adaptive_schedule(plan_id)
        
        return jsonify({
            'message': 'Schedule adapted successfully',
            'plan': plan.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to adapt schedule: {str(e)}'}), 500
