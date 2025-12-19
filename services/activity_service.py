"""
Activity service for tracking user actions
"""
from models import db, Activity
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
            db.session.add(activity)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def get_user_activities(user_id, limit=20):
        """Get recent activities for a user"""
        return Activity.query.filter_by(user_id=user_id).order_by(Activity.created_at.desc()).limit(limit).all()
