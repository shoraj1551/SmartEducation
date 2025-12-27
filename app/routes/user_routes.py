"""
User routes for SmartEducation API - Activities and Preferences
"""
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from app.models import User, Schedule, UserSession
from app.services.auth_service import AuthService
from app.services.activity_service import ActivityService

from bson import ObjectId

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Handle Bearer token format
        if token.startswith('Bearer '):
            token = token[7:]
            
        user_id = AuthService.verify_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid or expired'}), 401
            
        try:
            uid = ObjectId(user_id) if isinstance(user_id, str) else user_id
            current_user = User.objects(id=uid).first()
        except:
             return jsonify({'error': 'Invalid User ID'}), 401

        if not current_user:
            return jsonify({'error': 'User not found'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@user_bp.route('/activities', methods=['GET'])
@token_required
def get_activities(current_user):
    """Get recent activities for the current user"""
    limit = request.args.get('limit', 20, type=int)
    activities = ActivityService.get_user_activities(current_user.id, limit)
    return jsonify([a.to_dict() for a in activities])

@user_bp.route('/log-activity', methods=['POST'])
@token_required
def log_activity(current_user):
    """Manually log an activity from the frontend"""
    data = request.get_json()
    if not data or 'type' not in data:
        return jsonify({'error': 'Activity type is required'}), 400
        
    success = ActivityService.log_activity(
        current_user.id,
        data['type'],
        data.get('description'),
        data.get('metadata')
    )
    
    if success:
        return jsonify({'message': 'Activity logged successfully'}), 201
    return jsonify({'error': 'Failed to log activity'}), 500

@user_bp.route('/session-status', methods=['GET'])
@token_required
def get_session_status(current_user):
    """Find the last significant activity to prompt for session resumption"""
    from app.models import Activity
    # Look for last activity that wasn't just a 'login'
    last_activity = Activity.objects(
        user_id=current_user.id,
        activity_type__ne='login'
    ).order_by('-created_at').first()
    
    if last_activity:
        return jsonify({
            'has_previous_session': True,
            'last_activity': last_activity.to_dict()
        })
    
    return jsonify({'has_previous_session': False})

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Fetch full user profile"""
    return jsonify(current_user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile fields"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # List of allowed fields to update
    updatable_fields = [
        'name', 'job_title', 'bio', 'profile_picture', 
        'education_info', 'linkedin_url', 'github_url', 'website_url',
        'learning_goal', 'interests', 'commitment_level', 'expertise_level'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(current_user, field, data[field])
            
    try:
        current_user.save()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile-picture', methods=['POST'])
@token_required
def update_profile_picture(current_user):
    """
    Handle profile picture upload.
    Expects multipart/form-data with key 'profile_picture'.
    """
    import os
    from werkzeug.utils import secure_filename
    from datetime import datetime

    if 'profile_picture' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
    if file and allowed_file(file.filename):
        try:
            # Secure filename with timestamp to prevent cache issues and collisions
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"user_{current_user.id}_{timestamp}.{ext}")
            
            # Ensure directory exists (relative to app root)
            # app/../static/uploads/avatars
            save_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'avatars')
            os.makedirs(save_dir, exist_ok=True)
            
            file_path = os.path.join(save_dir, filename)
            file.save(file_path)
            
            # Update user profile
            relative_url = f"/static/uploads/avatars/{filename}"
            current_user.profile_picture = relative_url
            current_user.save()
            
            # Log activity
            ActivityService.log_activity(current_user.id, 'profile_picture_update', 'Updated profile picture')
            
            return jsonify({
                'message': 'Profile picture updated',
                'url': relative_url
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

@user_bp.route('/onboarding', methods=['POST'])
@token_required
def save_onboarding(current_user):
    """Save onboarding survey preferences (IMPROVEMENT-001)"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # NEW Survey Fields (IMPROVEMENT-001)
    if 'user_role' in data:
        current_user.user_role = data['user_role']
    if 'learning_goals' in data:
        current_user.learning_goals = data['learning_goals']
    if 'learning_type' in data:
        current_user.learning_type = data['learning_type']
    if 'deadline_type' in data:
        current_user.deadline_type = data['deadline_type']
    if 'daily_time_commitment' in data:
        current_user.daily_time_commitment = data['daily_time_commitment']
    if 'learning_blockers' in data:
        current_user.learning_blockers = data['learning_blockers']
    
    # Also save to OLD fields for backward compatibility
    # Map new fields to old structure
    if current_user.user_role:
        current_user.learning_goal = current_user.user_role
    if current_user.learning_goals:
        current_user.interests = current_user.learning_goals
    if current_user.daily_time_commitment:
        current_user.commitment_level = current_user.daily_time_commitment
        
    try:
        current_user.save()
        
        # Log activity
        ActivityService.log_activity(
            current_user.id,
            'onboarding_complete',
            'User completed the onboarding survey',
            {'survey_data': data}
        )
        
        return jsonify({
            'message': 'Onboarding data saved successfully',
            'user': current_user.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/preferences', methods=['GET'])
@token_required
def get_preferences(current_user):
    """Fetch user preferences"""
    return jsonify({
        'theme_preference': current_user.theme_preference,
        'email_notifications': current_user.email_notifications,
        'mobile_notifications': current_user.mobile_notifications,
        'marketing_emails': current_user.marketing_emails,
        'preferred_learning_time': current_user.preferred_learning_time,
        'daily_reminders': current_user.daily_reminders,
        'ai_insights': current_user.ai_insights,
        'community_milestones': current_user.community_milestones,
        'reduced_motion': current_user.reduced_motion,
        'high_contrast': current_user.high_contrast,
        'timezone': current_user.timezone if hasattr(current_user, 'timezone') else 'UTC'
    })

@user_bp.route('/preferences', methods=['PUT'])
@token_required
def update_preferences(current_user):
    """Update user preferences"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Allowed preference fields
    pref_fields = [
        'theme_preference', 'email_notifications', 
        'mobile_notifications', 'marketing_emails',
        'preferred_learning_time', 'daily_reminders',
        'ai_insights', 'community_milestones',
        'reduced_motion', 'high_contrast', 'timezone'
    ]
    
    for field in pref_fields:
        if field in data:
            setattr(current_user, field, data[field])
            
    try:
        current_user.save()
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': {
                'theme_preference': current_user.theme_preference,
                'email_notifications': current_user.email_notifications,
                'mobile_notifications': current_user.mobile_notifications,
                'marketing_emails': current_user.marketing_emails,
                'preferred_learning_time': current_user.preferred_learning_time,
                'daily_reminders': current_user.daily_reminders,
                'ai_insights': current_user.ai_insights,
                'community_milestones': current_user.community_milestones,
                'reduced_motion': current_user.reduced_motion,
                'high_contrast': current_user.high_contrast
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/schedules', methods=['GET'])
@token_required
def get_schedules(current_user):
    """Fetch all schedules for the current user"""
    schedules = Schedule.objects(user_id=current_user.id).order_by('-start_time')
    return jsonify([s.to_dict() for s in schedules])

@user_bp.route('/schedules', methods=['POST'])
@token_required
def add_schedule(current_user):
    """Add a new learning schedule/task"""
    from datetime import datetime
    data = request.get_json()
    if not data or 'title' not in data or 'start_time' not in data:
        return jsonify({'error': 'Title and start time are required'}), 400
        
    try:
        schedule = Schedule(
            user_id=current_user,
            title=data['title'],
            description=data.get('description'),
            start_time=datetime.fromisoformat(data['start_time'].replace('Z', '+00:00')),
            end_time=datetime.fromisoformat(data['end_time'].replace('Z', '+00:00')) if data.get('end_time') else None,
            repeat_pattern=data.get('repeat_pattern')
        )
        schedule.save()
        
        # Log activity
        ActivityService.log_activity(
            current_user.id,
            'add_schedule',
            f'Added schedule: {schedule.title}'
        )
        
        return jsonify(schedule.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/schedules/<schedule_id>', methods=['PUT'])
@token_required
def update_schedule(current_user, schedule_id):
    """Update an existing schedule"""
    data = request.get_json()
    schedule = Schedule.objects(id=schedule_id, user_id=current_user.id).first()
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
        
    if 'title' in data: schedule.title = data['title']
    if 'description' in data: schedule.description = data['description']
    if 'is_completed' in data: schedule.is_completed = data['is_completed']
    
    try:
        schedule.save()
        return jsonify(schedule.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/achievements', methods=['GET'])
@token_required
def get_achievements(current_user):
    """Fetch earned achievements and check for new ones"""
    from app.services.achievement_service import AchievementService
    
    # Auto-init if empty
    if AchievementService.get_all_achievements().count() == 0:
        AchievementService.initialize_achievements()
        
    # Proactive check
    AchievementService.check_milestones(current_user)
    
    earned = AchievementService.get_user_achievements(current_user.id)
    return jsonify([a.to_dict() for a in earned])

@user_bp.route('/achievements/available', methods=['GET'])
@token_required
def get_available_achievements(current_user):
    """Fetch all possible achievements"""
    from app.services.achievement_service import AchievementService
    all_ach = AchievementService.get_all_achievements()
    return jsonify([a.to_dict() for a in all_ach])

@user_bp.route('/schedules/<schedule_id>', methods=['DELETE'])
@token_required
def delete_schedule(current_user, schedule_id):
    """Delete a schedule"""
    schedule = Schedule.objects(id=schedule_id, user_id=current_user.id).first()
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
        
    schedule.delete()
    return jsonify({'message': 'Schedule deleted successfully'})

# Feature 3.1: Settings Expansion

@user_bp.route('/export', methods=['GET'])
@token_required
def export_user_data(current_user):
    """Export user data as JSON"""
    # Collect data
    from app.models import Schedule, Activity
    from app.services.achievement_service import AchievementService
    
    schedules = Schedule.objects(user_id=current_user.id)
    activities = Activity.objects(user_id=current_user.id).limit(100) # Limit for sanity
    achievements = AchievementService.get_user_achievements(current_user.id)
    
    data = {
        'profile': current_user.to_dict(),
        'schedules': [s.to_dict() for s in schedules],
        'recent_activities': [a.to_dict() for a in activities],
        'achievements': [a.to_dict() for a in achievements],
        'exported_at': datetime.utcnow().isoformat()
    }
    
    return jsonify(data)

@user_bp.route('/sessions', methods=['GET'])
@token_required
def get_sessions(current_user):
    """Get active sessions for user"""
    from app.models import UserSession
    sessions = UserSession.objects(user_id=current_user, is_active=True).order_by('-login_time').limit(3)
    
    # Enrich with current session flag
    token = request.headers.get('Authorization').split(' ')[1]
    current_sid = AuthService.get_token_payload(token).get('sid')
    
    results = []
    for s in sessions:
        s_dict = s.to_dict()
        if s.session_id == current_sid:
            s_dict['is_current'] = True
        results.append(s_dict)
        
    return jsonify(results)

@user_bp.route('/sessions/<session_id>', methods=['DELETE'])
@token_required
def revoke_session(current_user, session_id):
    """Revoke a specific session"""
    from app.models import UserSession
    
    # Allow revoking by ID or session_id string
    session = UserSession.objects(session_id=session_id, user_id=current_user).first()
    if not session:
        # Try object ID
        try:
             session = UserSession.objects(id=session_id, user_id=current_user).first()
        except:
            pass
            
    if not session:
        return jsonify({'error': 'Session not found'}), 404
        
    session.is_active = False
    session.save()
    
    return jsonify({'message': 'Session revoked successfully'})
