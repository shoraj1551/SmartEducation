from flask import Blueprint, request, jsonify, g
from app.models import User
from app.routes.security_routes import login_required # Reuse login check
from app.services.orchestrator_service import OrchestratorService

preference_bp = Blueprint('preference_bp', __name__)

@preference_bp.route('/api/preferences/update', methods=['POST'])
@login_required
def update_preferences():
    """Update user learning preferences"""
    data = request.get_json()
    user = g.user
    
    # 1. Learning Time
    if 'preferred_learning_time' in data:
        # Validate against known types (Morning, Deep Focus, Night)
        val = data['preferred_learning_time'].lower()
        if 'morning' in val: user.preferred_learning_time = 'morning'
        elif 'deep' in val or 'focus' in val: user.preferred_learning_time = 'deep_focus'
        elif 'night' in val: user.preferred_learning_time = 'night'
        # else keep existing or default? let's stick to valid ones.
        
    # 2. Engagement Toggles
    if 'daily_reminders' in data:
        user.daily_reminders = bool(data['daily_reminders'])
        
    if 'ai_insights' in data:
        user.ai_insights = bool(data['ai_insights'])
        
    if 'community_milestones' in data:
        user.community_milestones = bool(data['community_milestones'])
        
    # 3. Interface Style
    if 'reduced_motion' in data:
        user.reduced_motion = bool(data['reduced_motion'])
        
    if 'high_contrast' in data:
        user.high_contrast = bool(data['high_contrast'])
        
    try:
        user.save()
        
        # Return new orchestrator config immediately so frontend can adapt
        window = OrchestratorService.get_learning_window(user)
        ai_config = OrchestratorService.get_ai_config(user)
        
        return jsonify({
            'status': 'SUCCESS',
            'message': 'Preferences updated',
            'config': {
                'window': window,
                'ai_personality': ai_config
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@preference_bp.route('/api/preferences/config', methods=['GET'])
@login_required
def get_preferences_config():
    """Get current orchestration config"""
    window = OrchestratorService.get_learning_window(g.user)
    ai_config = OrchestratorService.get_ai_config(g.user)
    
    return jsonify({
        'window': window,
        'ai_personality': ai_config,
        'prefs': {
            'time': g.user.preferred_learning_time,
            'reminders': g.user.daily_reminders,
            'ai_insights': g.user.ai_insights
        }
    })
