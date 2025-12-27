"""
Schedule/Calendar Routes for SmartEducation
"""
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.models import User
from datetime import datetime
from mongoengine import DoesNotExist

schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/schedule')

def token_required(f):
    """Decorator to require authentication token"""
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
            
            return f(user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    decorated.__name__ = f.__name__
    return decorated

@schedule_bp.route('/events', methods=['GET'])
@token_required
def get_events(user_id):
    """
    Get calendar events for a time range
    Query params: start (ISO datetime), end (ISO datetime)
    """
    try:
        from app.models import Schedule, User
        from mongoengine import DoesNotExist
        
        start_str = request.args.get('start')
        end_str = request.args.get('end')
        
        if not start_str or not end_str:
            return jsonify({'error': 'start and end parameters are required'}), 400
        
        # Parse datetime strings
        start_time = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        # Get user object
        try:
            user = User.objects.get(id=user_id)
        except DoesNotExist:
            return jsonify({'error': 'User not found'}), 404
        
        # Query actual calendar events from database
        schedules = Schedule.objects(
            user_id=user,
            start_time__gte=start_time,
            start_time__lte=end_time
        ).order_by('start_time')
        
        # Convert to dict format
        events = []
        for schedule in schedules:
            event = {
                'id': str(schedule.id),
                'title': schedule.title,
                'description': schedule.description or '',
                'start_time': schedule.start_time.isoformat() if schedule.start_time else None,
                'end_time': schedule.end_time.isoformat() if schedule.end_time else None,
                'meeting_url': schedule.meeting_url if hasattr(schedule, 'meeting_url') else None
            }
            events.append(event)
        
        return jsonify({
            'events': events,
            'count': len(events)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid datetime format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to fetch events: {str(e)}'}), 500
