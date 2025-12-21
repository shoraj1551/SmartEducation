"""
Activity service for tracking user actions
"""
from app.models import Activity
import json

class ActivityService:
    """Service for logging and retrieving user activities"""
    
    @staticmethod
    def log_activity(user_id, activity_type, description=None, metadata=None):
        """Log a new user activity"""
        try:
            activity = Activity(
                user_id=user_id,
                activity_type=activity_type,
                description=description,
                metadata_json=json.dumps(metadata) if metadata else None
            )
            activity.save()
            return True
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            return False

    @staticmethod
    def get_user_activities(user_id, limit=20):
        """Get recent activities for a user"""
        return Activity.objects(user_id=user_id).order_by('-created_at').limit(limit)
