
"""
Gamification Routes (Feature 9)
API for XP, Level, and Progress data.
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.gamification_service import GamificationService
from functools import wraps

gamification_bp = Blueprint('gamification', __name__, url_prefix='/api/gamification')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            if token.startswith('Bearer '): token = token[7:]
            user_id = AuthService.verify_token(token)
            if not user_id: return jsonify({'error': 'Invalid token'}), 401
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Token error'}), 401
    return decorated

@gamification_bp.route('/progress', methods=['GET'])
@token_required
def get_progress(user_id):
    """Get current user level and XP progress"""
    try:
        data = GamificationService.get_progress(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/stats/weekly', methods=['GET'])
@token_required
def get_weekly_stats(user_id):
    """Get last 7 days of daily stats (Phase 29)"""
    from app.services.stats_service import StatsService
    try:
        data = StatsService.get_weekly_stats(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
