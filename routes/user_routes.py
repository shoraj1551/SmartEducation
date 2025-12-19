"""
User routes for SmartEducation API - Activities and Preferences
"""
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from models import User
from services.auth_service import AuthService
from services.activity_service import ActivityService

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
            
        current_user = User.objects(id=user_id).first()
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
    from models import Activity
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
        'education_info', 'linkedin_url', 'github_url', 'website_url'
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

@user_bp.route('/preferences', methods=['GET'])
@token_required
def get_preferences(current_user):
    """Fetch user preferences"""
    return jsonify({
        'theme_preference': current_user.theme_preference,
        'email_notifications': current_user.email_notifications,
        'mobile_notifications': current_user.mobile_notifications,
        'marketing_emails': current_user.marketing_emails
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
        'mobile_notifications', 'marketing_emails'
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
                'marketing_emails': current_user.marketing_emails
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
