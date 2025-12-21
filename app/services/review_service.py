
"""
Weekly Review Service (Feature 8)
Aggregates performance data for weekly summaries.
"""
from datetime import datetime, timedelta
from app.models import DailyTask
import calendar

class WeeklyReviewService:
    
    @staticmethod
    def get_weekly_summary(user_id):
        """
        Get summary for the last 7 days.
        """
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=7)
        
        tasks_completed = DailyTask.objects(
            user_id=user_id,
            completed_at__gte=week_start
        )
        
        total_minutes = 0
        completed_count = len(tasks_completed)
        
        # Find Most Productive Day
        daily_dist = {}
        for t in tasks_completed:
            total_minutes += t.actual_duration_minutes
            day_name = t.completed_at.strftime('%A')
            daily_dist[day_name] = daily_dist.get(day_name, 0) + t.actual_duration_minutes
            
        if daily_dist:
            most_productive_day = max(daily_dist, key=daily_dist.get)
        else:
            most_productive_day = "N/A"
            
        # Completion Rate (Created vs Completed in window)
        # Note: This is tricky if tasks were created earlier. 
        # Let's count tasks *scheduled* in this window.
        tasks_scheduled = DailyTask.objects(
            user_id=user_id,
            scheduled_date__gte=week_start,
            scheduled_date__lte=today
        ).count()
        
        rate = 0
        if tasks_scheduled > 0:
            rate = int((completed_count / tasks_scheduled) * 100)
            
        return {
            'period_start': week_start.isoformat(),
            'period_end': today.isoformat(),
            'total_hours': round(total_minutes / 60, 1),
            'tasks_completed': completed_count,
            'completion_rate': rate,
            'most_productive_day': most_productive_day,
            'status': 'ready' # or 'pending' if it's not Sunday (logic handled by caller or here)
        }
