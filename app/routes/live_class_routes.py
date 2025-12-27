"""
Live Class Routes
API endpoints for managing live online classes
"""
from flask import Blueprint, request, jsonify
from app.services.live_class_service import LiveClassService
from app.services.auth_service import AuthService
from functools import wraps
from datetime import datetime

live_class_bp = Blueprint('live_class', __name__, url_prefix='/api/live-class')


def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_id = AuthService.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Add user_id to kwargs
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated


@live_class_bp.route('/join', methods=['POST'])
@token_required
def join_class(user_id):
    """Create and join a live class"""
    try:
        data = request.get_json()
        
        if not data or 'meeting_url' not in data:
            return jsonify({'error': 'Meeting URL is required'}), 400
        
        # Create live class record
        live_class = LiveClassService.create_class(
            user_id=user_id,
            meeting_url=data['meeting_url'],
            title=data.get('title'),
            platform=data.get('platform', 'custom'),
            description=data.get('description', ''),
            meeting_id=data.get('meeting_id', ''),
            passcode=data.get('passcode', ''),
            scheduled_at=data.get('scheduled_at'),
            duration_minutes=data.get('duration_minutes', 60),
            tags=data.get('tags', []),
            category=data.get('category', '')
        )
        
        # Mark as joined
        live_class = LiveClassService.join_class(str(live_class.id), user_id)
        
        return jsonify({
            'message': 'Joining class...',
            'class': live_class.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to join class: {str(e)}'}), 500


@live_class_bp.route('/classes', methods=['GET'])
@token_required
def get_classes(user_id):
    """Get all live classes for the user"""
    try:
        limit = request.args.get('limit', type=int)
        skip = request.args.get('skip', default=0, type=int)
        
        classes = LiveClassService.get_user_classes(
            user_id=user_id,
            limit=limit,
            skip=skip
        )
        
        return jsonify({
            'classes': [c.to_dict() for c in classes],
            'count': len(classes)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch classes: {str(e)}'}), 500


@live_class_bp.route('/upcoming', methods=['GET'])
@token_required
def get_upcoming(user_id):
    """Get upcoming scheduled classes"""
    try:
        classes = LiveClassService.get_upcoming_classes(user_id)
        
        return jsonify({
            'classes': [c.to_dict() for c in classes],
            'count': len(classes)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch upcoming classes: {str(e)}'}), 500


@live_class_bp.route('/past', methods=['GET'])
@token_required
def get_past(user_id):
    """Get past classes (recordings)"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        classes = LiveClassService.get_past_classes(user_id, limit=limit)
        
        return jsonify({
            'classes': [c.to_dict() for c in classes],
            'count': len(classes)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch past classes: {str(e)}'}), 500


@live_class_bp.route('/classes/<class_id>/end', methods=['POST'])
@token_required
def end_class(user_id, class_id):
    """Mark a class as ended"""
    try:
        live_class = LiveClassService.end_class(class_id, user_id)
        
        return jsonify({
            'message': 'Class ended',
            'class': live_class.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to end class: {str(e)}'}), 500
