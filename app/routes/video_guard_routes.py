"""
Video Guard Routes for Feature 7: Anti-Distraction Video Learning Guard
API endpoints for video access control
"""
from flask import Blueprint, request, jsonify
from app.services.video_guard_service import VideoGuardService
from app.services.auth_service import AuthService
from functools import wraps

video_guard_bp = Blueprint('video_guard', __name__, url_prefix='/api/video-guard')


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


@video_guard_bp.route('/allowed-videos/<item_id>', methods=['GET'])
@token_required
def get_allowed_videos(user_id, item_id):
    """Get whitelisted videos for a learning item"""
    try:
        videos = VideoGuardService.get_allowed_videos(item_id)
        
        return jsonify({'videos': videos}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get allowed videos: {str(e)}'}), 500


@video_guard_bp.route('/whitelist/<item_id>', methods=['POST'])
@token_required
def create_whitelist(user_id, item_id):
    """Create video whitelist for a learning item"""
    try:
        data = request.get_json()
        
        if not data or 'video_urls' not in data:
            return jsonify({'error': 'video_urls is required'}), 400
        
        item = VideoGuardService.create_video_whitelist(item_id, data['video_urls'])
        
        return jsonify({
            'message': 'Whitelist created successfully',
            'item_id': str(item.id)
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to create whitelist: {str(e)}'}), 500


@video_guard_bp.route('/track-watch', methods=['POST'])
@token_required
def track_watch(user_id):
    """Track video watch progress"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data or 'video_url' not in data:
            return jsonify({'error': 'learning_item_id and video_url are required'}), 400
        
        item = VideoGuardService.track_video_watch(
            learning_item_id=data['learning_item_id'],
            video_url=data['video_url'],
            watch_data=data.get('watch_data', {})
        )
        
        return jsonify({'message': 'Watch progress tracked'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to track watch: {str(e)}'}), 500


@video_guard_bp.route('/report-distraction', methods=['POST'])
@token_required
def report_distraction(user_id):
    """Log distraction attempt"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        item = VideoGuardService.log_distraction_attempt(
            learning_item_id=data['learning_item_id'],
            distraction_type=data.get('distraction_type', 'navigation'),
            details=data.get('details')
        )
        
        return jsonify({'message': 'Distraction logged'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to log distraction: {str(e)}'}), 500


@video_guard_bp.route('/stats/<item_id>', methods=['GET'])
@token_required
def get_video_stats(user_id, item_id):
    """Get video watching statistics"""
    try:
        stats = VideoGuardService.get_video_stats(item_id)
        
        return jsonify({'stats': stats}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500


@video_guard_bp.route('/validate/<item_id>', methods=['POST'])
@token_required
def validate_video(user_id, item_id):
    """Validate if a video is allowed"""
    try:
        data = request.get_json()
        
        if not data or 'video_url' not in data:
            return jsonify({'error': 'video_url is required'}), 400
        
        is_allowed = VideoGuardService.is_video_allowed(item_id, data['video_url'])
        
        return jsonify({
            'allowed': is_allowed,
            'message': 'Video is allowed' if is_allowed else 'Video is not in whitelist'
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to validate video: {str(e)}'}), 500
