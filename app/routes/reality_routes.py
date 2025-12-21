"""
Reality Metrics Routes for Feature 6: Reality-Driven Progress Visualization
API endpoints for honest progress metrics
"""
from flask import Blueprint, request, jsonify
from app.services.reality_metrics_service import RealityMetricsService
from app.services.auth_service import AuthService
from functools import wraps

reality_bp = Blueprint('reality', __name__, url_prefix='/api/metrics')


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


@reality_bp.route('/reality/<item_id>', methods=['GET'])
@token_required
def get_reality_metrics(user_id, item_id):
    """Get reality metrics for a learning item"""
    try:
        metrics = RealityMetricsService.calculate_reality_metrics(item_id)
        
        return jsonify({'metrics': metrics}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get reality metrics: {str(e)}'}), 500


@reality_bp.route('/wasted-time', methods=['GET'])
@token_required
def get_wasted_time(user_id):
    """Get wasted time analysis"""
    try:
        days = request.args.get('days', default=30, type=int)
        analysis = RealityMetricsService.get_wasted_time_analysis(user_id, days)
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get wasted time analysis: {str(e)}'}), 500


@reality_bp.route('/progress-history/<item_id>', methods=['GET'])
@token_required
def get_progress_history(user_id, item_id):
    """Get progress history timeline"""
    try:
        days = request.args.get('days', default=30, type=int)
        timeline = RealityMetricsService.get_progress_history(item_id, days)
        
        return jsonify({'timeline': timeline}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get progress history: {str(e)}'}), 500
