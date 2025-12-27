
"""
Stats Service (Phase 29)
Manages pre-aggregated statistics for high-performance dashboards.
"""
from app.models import DailyStat, User
from datetime import datetime, timedelta

class StatsService:
    
    @staticmethod
    def update_daily_stats(user_id, minutes_spent):
        """
        Increment daily stats when a session is completed.
        Write-Through Caching Pattern.
        """
        try:
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Atomic update using mongoengine/mongodb
            # If document doesn't exist, upsert=True will create it
            stat = DailyStat.objects(user_id=user_id, date=today).modify(
                upsert=True,
                new=True,
                inc__total_minutes=minutes_spent,
                inc__sessions_count=1
            )
            return stat
        except Exception as e:
            print(f"Stats Update Error: {e}")
            return None

    @staticmethod
    def get_weekly_stats(user_id):
        """
        Get last 7 days of stats for the dashboard chart.
        Read-Optimized: Fetches 7 pre-calculated docs instead of scanning history.
        """
        try:
            end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            start_date = end_date - timedelta(days=6) # 7 days total including today
            
            stats = DailyStat.objects(
                user_id=user_id, 
                date__gte=start_date, 
                date__lte=end_date
            ).order_by('date')
            
            # Normalize to ensure all days are represented (even if 0)
            result = []
            stats_map = {s.date.strftime('%Y-%m-%d'): s.total_minutes for s in stats}
            
            current = start_date
            while current <= end_date:
                date_str = current.strftime('%Y-%m-%d')
                day_name = current.strftime('%a') # Mon, Tue
                hours = round(stats_map.get(date_str, 0) / 60, 1) # Convert min to hours
                
                result.append({
                    'day': day_name,
                    'date': date_str,
                    'hours': hours
                })
                current += timedelta(days=1)
                
            return result
        except Exception as e:
            print(f"Stats Fetch Error: {e}")
            return []
