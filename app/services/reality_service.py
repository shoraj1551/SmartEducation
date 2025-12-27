
"""
Reality Service for "Reality Check" Logic
Validates if learning plans are mathematically feasible.
"""
from datetime import datetime
from app.models import LearningItem, User
from mongoengine.errors import DoesNotExist

class RealityService:
    """
    Service to perform 'Reality Checks' on proposed learning commitments.
    Ensures users don't set themselves up for failure.
    """
    
    BUFFER_PERCENTAGE = 1.2  # 20% buffer for re-watching/notes
    
    @staticmethod
    def check_feasibility(user_id, learning_item_id, target_date, daily_minutes, study_days_per_week=5):
        """
        Check if a study plan is realistic.
        
        Args:
            user_id: User ID
            learning_item_id: ID of the content
            target_date: Proposed finish date (datetime)
            daily_minutes: Minutes user commits to study per day
            study_days_per_week: Number of study days per week (default 5)
            
        Returns:
            Dict containing:
            - is_feasible (bool)
            - message (str)
            - details (dict: required_minutes, available_minutes, surplus_minutes)
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
                
            try:
                item = LearningItem.objects.get(id=learning_item_id)
            except DoesNotExist:
                # Try to find string ID in Bookmarks
                from app.models import Bookmark
                # Ensure user_id usage matches model
                bookmark = Bookmark.objects.get(id=learning_item_id, user_id=user)
                
                # Create a temporary proxy object to emulate LearningItem for validation
                class ProxyItem:
                    def __init__(self, b):
                        self.total_duration = 0
                        # Try to find duration in metadata
                        if b.metadata:
                            # Check common duration paths
                            if 'video_meta' in b.metadata:
                                self.total_duration = b.metadata['video_meta'].get('duration', 0)
                            elif 'duration' in b.metadata:
                                self.total_duration = b.metadata['duration']
                            
                item = ProxyItem(bookmark)
                
        except DoesNotExist:
            return {'is_feasible': False, 'message': 'Invalid user or item'}

        # 1. Get Content Duration
        total_duration = item.total_duration
        if total_duration <= 0:
            # If duration is unknown, we can't do a strict math check.
            # We assume it's feasible but warn the user.
            return {
                'is_feasible': True, 
                'message': 'Content duration unknown. Plan passed, but proceed with caution.',
                'details': {'reason': 'unknown_duration'}
            }
            
        # 2. Calculate Required Time (with Buffer)
        required_minutes = total_duration * RealityService.BUFFER_PERCENTAGE
        
        # 3. Calculate Available Time
        today = datetime.utcnow()
        if target_date <= today:
             return {'is_feasible': False, 'message': 'Target date must be in the future'}
             
        total_days = (target_date - today).days
        weeks = total_days / 7
        total_study_days = weeks * study_days_per_week
        
        available_minutes = total_study_days * daily_minutes
        
        # 4. Compare
        surplus = available_minutes - required_minutes
        
        if surplus >= 0:
            return {
                'is_feasible': True,
                'message': 'Plan is realistic! You have a comfortable buffer.',
                'details': {
                    'required_hours': round(required_minutes / 60, 1),
                    'available_hours': round(available_minutes / 60, 1),
                    'buffer_hours': round(surplus / 60, 1)
                }
            }
        else:
            shortfall = abs(surplus)
            return {
                'is_feasible': False,
                'message': (
                    f"Plan is unrealistic. You need {round(required_minutes/60, 1)} hours "
                    f"but only have {round(available_minutes/60, 1)} available. "
                    f"Increase daily time or extend the date."
                ),
                'details': {
                    'required_hours': round(required_minutes / 60, 1),
                    'available_hours': round(available_minutes / 60, 1),
                    'shortfall_hours': round(shortfall / 60, 1)
                }
            }

    @staticmethod
    def calculate_truth_metrics(user_id):
        """
        Calculate the 'Truth' metrics: Days Wasted, Actual Velocity, and Real Finish Date.
        """
        from app.models import DailyTask, Commitment, LearningItem
        from datetime import timedelta
        
        today = datetime.utcnow().date()
        
        # 1. Calculate Days Wasted (Last 30 Days)
        # Definition: A day with < 5 minutes of study is wasted.
        days_wasted = 0
        days_invested = 0
        start_check_date = today - timedelta(days=30)
        
        # Get all tasks completed in last 30 days
        recent_tasks = DailyTask.objects(
            user_id=user_id,
            completed_at__gte=start_check_date
        )
        
        # Group by date
        daily_effort = {}
        for i in range(31):
            date_key = (start_check_date + timedelta(days=i)).isoformat()
            daily_effort[date_key] = 0
            
        for task in recent_tasks:
            if task.completed_at:
                d_key = task.completed_at.date().isoformat()
                if d_key in daily_effort:
                    daily_effort[d_key] += task.actual_duration_minutes
                    
        # Count Zero Days (skipping future or today if not over yet? simpler logic for now)
        # Note: We only count days up to yesterday to be fair, or include today if 0.
        # Let's count up to TODAY (inclusive) but maybe today isn't wasted yet? 
        # Strict Mode: Today is wasted until you work.
        for date_str, minutes in daily_effort.items():
            if minutes < 5:
                # Check if this date is substantially in the past (not future)
                if date_str <= today.isoformat():
                     days_wasted += 1
            else:
                days_invested += 1
                
        # 2. Calculate Velocity (Avg min/day over last 7 days)
        velocity_window = 7
        velocity_minutes = 0
        v_start = today - timedelta(days=velocity_window)
        
        for task in recent_tasks:
            if task.completed_at and task.completed_at.date() >= v_start:
                velocity_minutes += task.actual_duration_minutes
                
        actual_velocity = velocity_minutes / velocity_window # min/day
        
        # 3. Project Finish Dates for Active Commitments
        commitments = Commitment.objects(user_id=user_id, status='active')
        projections = []
        
        for comm in commitments:
            item = comm.learning_item_id
            remaining_mins = (item.total_duration - item.completed_duration) * RealityService.BUFFER_PERCENTAGE
            
            if actual_velocity > 0:
                days_needed = remaining_mins / actual_velocity
            else:
                days_needed = 9999 # Infinite
                
            real_finish_date = today + timedelta(days=int(days_needed))
            
            # Gap
            target_date = comm.target_completion_date.date()
            gap_days = (real_finish_date - target_date).days
            
            projections.append({
                'title': item.title,
                'target_date': target_date.isoformat(),
                'real_date': real_finish_date.isoformat(),
                'gap_days': gap_days,
                'status': 'on_track' if gap_days <= 0 else 'delayed'
            })
            
        return {
            'days_wasted': days_wasted,
            'days_invested': days_invested,
            'actual_velocity': round(actual_velocity, 1),
            'projections': projections
        }
