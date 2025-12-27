
"""
Focus Routes (Feature 5: Deep Focus Mode)
API endpoints for managing focus sessions, timer logic, and distraction logging.
"""
from flask import Blueprint, jsonify, request, render_template
from app.services.auth_service import AuthService
from app.models import FocusSession, DailyTask, LearningItem
from datetime import datetime

focus_bp = Blueprint('focus', __name__) # Prefix is handled in registration or here? 
# Note: Main routes usually handle HTML rendering at root/subpath, while api routes are at /api/.
# I will separate: 
# 1. HTML route: /focus (renders the player)
# 2. API route: /api/focus/* (handles data)

# --- HTML Routes ---
@focus_bp.route('/focus')
def focus_player():
    """Render the Focus Mode Player"""
    return render_template('focus.html')

# --- API Routes ---
@focus_bp.route('/api/focus/start', methods=['POST'])
def start_session():
    """Start a new focus session"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = AuthService.verify_token(token)
        if not user_id: return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        item_id = data.get('learning_item_id')
        task_id = data.get('daily_task_id') # Optional
        
        # Auto-resolve item_id from task_id if missing
        if not item_id and task_id:
            try:
                task = DailyTask.objects.get(id=task_id)
                item_id = task.learning_item_id.id
            except Exception:
                return jsonify({'error': 'Invalid daily_task_id'}), 400

        if not item_id:
            return jsonify({'error': 'learning_item_id is required'}), 400
            
        # Close any existing active sessions for this user? (Optional cleanup)
        
        session = FocusSession(
            user_id=user_id,
            learning_item_id=item_id,
            daily_task_id=task_id,
            started_at=datetime.utcnow(),
            is_active=True
        )
        session.save()
        
            
        # If daily task, update status to in_progress
        if task_id:
            task = DailyTask.objects.get(id=task_id)
            task.status = 'in_progress'
            if not task.started_at:
                task.started_at = datetime.utcnow()
            task.save()
            
        # Get Item URL and Sanitize
        from app.services.video_guard_service import VideoGuardService
        item = LearningItem.objects.get(id=item_id)
        sanitized_url = VideoGuardService.sanitize_url(item.url) if item.url else None

        return jsonify({
            'message': 'Focus session started',
            'session_id': str(session.id),
            'content_url': sanitized_url,
            'title': item.title
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@focus_bp.route('/api/focus/end', methods=['POST'])
def end_session():
    """End a focus session"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = AuthService.verify_token(token)
        if not user_id: return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        session_id = data.get('session_id')
        duration_minutes = data.get('duration_minutes') # Trusted client duration or calc server side?
        
        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400
            
        session = FocusSession.objects.get(id=session_id, user_id=user_id)
        session.ended_at = datetime.utcnow()
        session.is_active = False
        session.exit_reason = data.get('reason', 'completed')
        
        # Calculate duration if not provided or double check
        # server_duration = (session.ended_at - session.started_at).total_seconds() / 60
        if duration_minutes:
            session.duration_minutes = int(duration_minutes)
            
        session.save()
        
        # Update Item Progress
        item = session.learning_item_id
        item.completed_duration += session.duration_minutes
        item.update_progress()
        item.last_accessed_at = datetime.utcnow()
        item.save()
        
        # Update Task if exists
        if session.daily_task_id:
            task = session.daily_task_id
            task.actual_duration_minutes += session.duration_minutes
            if data.get('mark_complete', False):
                task.mark_complete(task.actual_duration_minutes)
            task.save()
            
        # --- GAMIFICATION: AWARD XP ---
        from app.services.gamification_service import GamificationService
        xp_amount = int(session.duration_minutes * 10) # 10 XP per minute
        if data.get('mark_complete', False):
            xp_amount += 500 # Bonus for finishing task
            
        gamification_result = GamificationService.award_xp(user_id, xp_amount, "Focus Session")
        
        # --- PHASE 29: UPDATE DAILY STATS (Write-Through) ---
        from app.services.stats_service import StatsService
        StatsService.update_daily_stats(user_id, session.duration_minutes)
            
        return jsonify({
            'message': 'Session ended successfully',
            'duration_minutes': session.duration_minutes,
            'gamification': gamification_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@focus_bp.route('/api/focus/log-distraction', methods=['POST'])
def log_distraction():
    """Log a distraction attempt"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = AuthService.verify_token(token)
        if not user_id: return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        session_id = data.get('session_id')
        distraction_type = data.get('type', 'tab_switch')
        
        if not session_id: return jsonify({'error': 'session_id required'}), 400
        
        session = FocusSession.objects.get(id=session_id)
        session.log_distraction(distraction_type)
        
        return jsonify({'message': 'Distraction logged'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
