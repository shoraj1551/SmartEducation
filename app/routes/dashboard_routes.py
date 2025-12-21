
"""
Dashboard Routes (Feature 2 & 4 Integration)
API for fueling the main command center.
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.priority_service import PriorityService
from app.models import DailyTask, LearningItem
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/focus', methods=['GET'])
def get_focus_task():
    """
    GET THE ONE SINGLE FOCUS TASK (Intelligence Engine)
    Prioritizes:
    1. Overdue Daily Tasks (from Commitments)
    2. Today's Daily Tasks (from Commitments)
    3. Highest Priority Inbox Item (if no daily tasks)
    """
    # Token auth manual verify for speed/simplicity here (or adding decorator)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
    user_id = AuthService.verify_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    
    # 1. Check for OVERDUE tasks (Highest Urgency)
    overdue = DailyTask.objects(
        user_id=user_id,
        status='pending',
        scheduled_date__lt=today
    ).order_by('scheduled_date').first()
    
    if overdue:
        return jsonify({
            'type': 'daily_task',
            'title': overdue.title,
            'subtitle': f"Overdue from {overdue.scheduled_date.strftime('%b %d')}",
            'duration': overdue.estimated_duration_minutes,
            'reason': 'Catch Up (High Priority)',
            'id': str(overdue.id),
            'action': 'start_session'
        })
        
    # 2. Check for TODAY'S tasks (Commitment)
    todays_task = DailyTask.objects(
        user_id=user_id,
        status='pending',
        scheduled_date__gte=today,
        scheduled_date__lt=today.replace(hour=23, minute=59)
    ).order_by('-priority_score').first()
    
    if todays_task:
        return jsonify({
            'type': 'daily_task',
            'title': todays_task.title,
            'subtitle': 'Your Iron Commitment for Today',
            'duration': todays_task.estimated_duration_minutes,
            'reason': 'Daily Goal',
            'id': str(todays_task.id),
            'action': 'start_session'
        })
        
    # 3. Fallback: Top Inbox Item (Smart Priority)
    top_items = PriorityService.get_top_priorities(user_id, limit=1)
    if top_items:
        item = top_items[0]
        return jsonify({
            'type': 'learning_item',
            'title': item.title,
            'subtitle': f"{item.source_type.title()} • {item.total_duration} mins",
            'duration': item.total_duration,
            'reason': 'Smart Recommendation',
            'id': str(item.id),
            'action': 'view_item'
        })
        
    return jsonify({
        'type': 'empty',
        'title': 'All Caught Up!',
        'subtitle': 'Relax or add new content.',
        'action': 'add_content'
    })
