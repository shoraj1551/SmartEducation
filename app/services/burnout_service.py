
"""
Burnout Service (Feature 8)
Detects overwork patterns to prevent user exhaustion.
"""
from datetime import datetime, timedelta
from app.models import DailyTask

class BurnoutService:
    
    # Thresholds
    HIGH_INTENSITY_MINUTES = 240 # 4 hours
    CONSECUTIVE_DAYS_THRESHOLD = 5
    NO_REST_DAYS_THRESHOLD = 14
    
    @staticmethod
    def check_burnout_risk(user_id):
        """
        Analyze recent activity for burnout markers.
        Returns: { 'level': 'none'|'moderate'|'high', 'message': str }
        """
        today = datetime.utcnow().date()
        start_date = today - timedelta(days=21) # Look back 3 weeks max
        
        # valid_tasks = DailyTask.objects(
        #     user_id=user_id,
        #     completed_at__gte=start_date
        # )
        
        # But for efficiency, let's aggregate manually or via pipeline if needed.
        # Simple iteration for MVP is fine given user scale.
        tasks = DailyTask.objects(
             user_id=user_id,
             completed_at__gte=start_date
        )
        
        # 1. Aggregate Daily Minutes
        daily_minutes = {}
        # Pre-fill last 21 days with 0
        for i in range(22):
            d = (start_date + timedelta(days=i)).isoformat()
            daily_minutes[d] = 0
            
        for t in tasks:
            if t.completed_at:
                d = t.completed_at.date().isoformat()
                if d in daily_minutes:
                    daily_minutes[d] += t.actual_duration_minutes
                    
        # 2. Check for Consecutive High Intensity
        consecutive_high = 0
        max_consecutive_high = 0
        
        # Sort dates
        sorted_dates = sorted(daily_minutes.keys())
        # We only care about up to yesterday/today
        
        for d in sorted_dates:
            mins = daily_minutes[d]
            if mins >= BurnoutService.HIGH_INTENSITY_MINUTES:
                consecutive_high += 1
            else:
                max_consecutive_high = max(max_consecutive_high, consecutive_high)
                consecutive_high = 0
        max_consecutive_high = max(max_consecutive_high, consecutive_high)
        
        # 3. Check for No Rest (Days with > 0 minutes)
        consecutive_active = 0
        max_consecutive_active = 0
        
        for d in sorted_dates:
            mins = daily_minutes[d]
            if mins > 15: # Negligible work isn't work
                consecutive_active += 1
            else:
                max_consecutive_active = max(max_consecutive_active, consecutive_active)
                consecutive_active = 0
        max_consecutive_active = max(max_consecutive_active, consecutive_active)
        
        # 4. Determine Risk
        risk_level = 'none'
        message = "You are balanced."
        
        if max_consecutive_high >= BurnoutService.CONSECUTIVE_DAYS_THRESHOLD:
            risk_level = 'high'
            message = "⚠️ BURNOUT ALERT: You've worked 4+ hours for 5 days straight. Take a day off immediately."
        
        elif max_consecutive_active >= BurnoutService.NO_REST_DAYS_THRESHOLD:
            risk_level = 'moderate'
            message = "⚠️ REST REQUIRED: You haven't taken a break in 2 weeks. Schedule a zero day."
            
        elif max_consecutive_high >= 3:
            risk_level = 'moderate'
            message = "Pace yourself. High intensity detected."
            
        return {
            'level': risk_level,
            'message': message,
            'details': {
                'high_intensity_streak': max_consecutive_high,
                'active_streak': max_consecutive_active
            }
        }
