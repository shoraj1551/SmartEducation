"""
Reality Metrics Service for Feature 6: Reality-Driven Progress Visualization
Calculates honest, reality-based progress metrics
"""
from datetime import datetime, timedelta
from app.models import LearningItem, DailyTask, User
from mongoengine.errors import DoesNotExist
import math


class RealityMetricsService:
    """Service for calculating honest progress metrics"""
    
    @staticmethod
    def calculate_reality_metrics(learning_item_id):
        """
        Calculate comprehensive reality metrics for a learning item
        
        Returns:
            Dictionary with honest progress statistics
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        # Calculate all metrics
        actual_completion = RealityMetricsService._calculate_actual_completion(item)
        days_wasted = RealityMetricsService._calculate_days_wasted(item)
        expected_vs_actual = RealityMetricsService._calculate_expected_vs_actual(item)
        projected_finish = RealityMetricsService._calculate_projected_finish(item)
        efficiency_score = RealityMetricsService._calculate_efficiency_score(item)
        
        return {
            'actual_completion_percentage': actual_completion,
            'days_since_start': (datetime.utcnow() - item.added_at).days if item.added_at else 0,
            'days_active': RealityMetricsService._calculate_active_days(item),
            'days_wasted': days_wasted,
            'expected_progress': expected_vs_actual['expected'],
            'actual_progress': expected_vs_actual['actual'],
            'progress_gap': expected_vs_actual['gap'],
            'projected_finish_date': projected_finish['date'],
            'days_until_projected_finish': projected_finish['days_remaining'],
            'target_finish_date': item.target_completion_date.isoformat() if item.target_completion_date else None,
            'on_track': projected_finish['on_track'],
            'efficiency_score': efficiency_score,
            'status_message': RealityMetricsService._generate_status_message(item, efficiency_score, days_wasted)
        }
    
    @staticmethod
    def _calculate_actual_completion(item):
        """Calculate actual completion percentage"""
        return round(item.progress_percentage, 2)
    
    @staticmethod
    def _calculate_days_wasted(item):
        """
        Calculate days with zero progress (wasted days)
        """
        if not item.added_at:
            return 0
        
        days_since_start = (datetime.utcnow() - item.added_at).days
        
        # Get all tasks for this item
        tasks = DailyTask.objects(learning_item_id=item)
        
        # Count days with completed tasks
        active_days = set()
        for task in tasks:
            if task.completed_at:
                active_days.add(task.completed_at.date())
        
        # Wasted days = total days - active days
        wasted = days_since_start - len(active_days)
        return max(0, wasted)
    
    @staticmethod
    def _calculate_active_days(item):
        """Calculate number of days with actual progress"""
        tasks = DailyTask.objects(learning_item_id=item, status='completed')
        
        active_days = set()
        for task in tasks:
            if task.completed_at:
                active_days.add(task.completed_at.date())
        
        return len(active_days)
    
    @staticmethod
    def _calculate_expected_vs_actual(item):
        """
        Calculate expected vs actual progress
        """
        if not item.added_at or not item.target_completion_date:
            return {'expected': 0, 'actual': item.progress_percentage, 'gap': 0}
        
        # Calculate expected progress based on time elapsed
        total_days = (item.target_completion_date - item.added_at).days
        elapsed_days = (datetime.utcnow() - item.added_at).days
        
        if total_days <= 0:
            expected_progress = 100.0
        else:
            expected_progress = min(100.0, (elapsed_days / total_days) * 100)
        
        actual_progress = item.progress_percentage
        gap = actual_progress - expected_progress
        
        return {
            'expected': round(expected_progress, 2),
            'actual': round(actual_progress, 2),
            'gap': round(gap, 2)
        }
    
    @staticmethod
    def _calculate_projected_finish(item):
        """
        Calculate projected finish date based on current pace
        """
        if item.progress_percentage >= 100:
            return {
                'date': datetime.utcnow().isoformat(),
                'days_remaining': 0,
                'on_track': True
            }
        
        if not item.added_at or item.progress_percentage == 0:
            return {
                'date': None,
                'days_remaining': None,
                'on_track': False
            }
        
        # Calculate current pace (% per day)
        days_elapsed = (datetime.utcnow() - item.added_at).days
        if days_elapsed == 0:
            days_elapsed = 1
        
        pace_per_day = item.progress_percentage / days_elapsed
        
        if pace_per_day == 0:
            return {
                'date': None,
                'days_remaining': None,
                'on_track': False
            }
        
        # Calculate days needed to complete
        remaining_percentage = 100 - item.progress_percentage
        days_needed = remaining_percentage / pace_per_day
        
        projected_date = datetime.utcnow() + timedelta(days=days_needed)
        
        # Check if on track
        on_track = True
        if item.target_completion_date:
            on_track = projected_date <= item.target_completion_date
        
        return {
            'date': projected_date.isoformat(),
            'days_remaining': int(days_needed),
            'on_track': on_track
        }
    
    @staticmethod
    def _calculate_efficiency_score(item):
        """
        Calculate efficiency score (0-100)
        Higher = more efficient learning
        """
        if not item.added_at:
            return 50.0
        
        days_elapsed = (datetime.utcnow() - item.added_at).days
        if days_elapsed == 0:
            days_elapsed = 1
        
        # Efficiency = (progress made) / (time spent)
        efficiency = (item.progress_percentage / days_elapsed) * 10
        
        # Cap at 100
        return min(100.0, round(efficiency, 2))
    
    @staticmethod
    def _generate_status_message(item, efficiency_score, days_wasted):
        """Generate context-aware status message"""
        progress = item.progress_percentage
        
        if progress >= 90:
            return "🎉 Almost there! Finish strong!"
        elif progress >= 75:
            return "💪 Great progress! Keep the momentum going."
        elif progress >= 50:
            return "📈 Halfway there! Stay consistent."
        elif progress >= 25:
            if days_wasted > 7:
                return f"⚠️ {days_wasted} days wasted. Time to refocus!"
            else:
                return "🚀 Good start! Build your streak."
        else:
            if days_wasted > 14:
                return f"🔴 {days_wasted} days wasted. Serious action needed!"
            else:
                return "⏰ Just getting started. Stay committed!"
    
    @staticmethod
    def get_wasted_time_analysis(user_id, days=30):
        """
        Get wasted time analysis for all user's items
        
        Returns:
            Dictionary with wasted time breakdown
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return {}
        
        items = LearningItem.objects(user_id=user, status='active')
        
        total_wasted_days = 0
        item_breakdown = []
        
        for item in items:
            wasted = RealityMetricsService._calculate_days_wasted(item)
            total_wasted_days += wasted
            
            if wasted > 0:
                item_breakdown.append({
                    'item_id': str(item.id),
                    'title': item.title,
                    'days_wasted': wasted,
                    'progress': item.progress_percentage
                })
        
        # Sort by most wasted
        item_breakdown.sort(key=lambda x: x['days_wasted'], reverse=True)
        
        return {
            'total_wasted_days': total_wasted_days,
            'items_with_waste': len(item_breakdown),
            'breakdown': item_breakdown[:5],  # Top 5
            'wake_up_message': RealityMetricsService._generate_wake_up_message(total_wasted_days)
        }
    
    @staticmethod
    def _generate_wake_up_message(total_wasted_days):
        """Generate wake-up call message based on wasted time"""
        if total_wasted_days == 0:
            return "✅ Perfect! No wasted days."
        elif total_wasted_days <= 7:
            return f"⚠️ {total_wasted_days} days wasted. Stay focused!"
        elif total_wasted_days <= 30:
            return f"🔴 {total_wasted_days} days wasted. That's over a week of lost progress!"
        else:
            return f"🚨 {total_wasted_days} days wasted. That's over a month! Time for serious change."
    
    @staticmethod
    def get_progress_history(learning_item_id, days=30):
        """
        Get progress history timeline for an item
        
        Returns:
            List of progress snapshots over time
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        # Get completed tasks over time
        since_date = datetime.utcnow() - timedelta(days=days)
        tasks = DailyTask.objects(
            learning_item_id=item,
            status='completed',
            completed_at__gte=since_date
        ).order_by('completed_at')
        
        # Build timeline
        timeline = []
        cumulative_progress = 0
        
        for task in tasks:
            # Estimate progress contribution
            if item.total_duration > 0:
                progress_contribution = (task.estimated_duration_minutes / item.total_duration) * 100
                cumulative_progress += progress_contribution
            
            timeline.append({
                'date': task.completed_at.date().isoformat(),
                'task_title': task.title,
                'cumulative_progress': min(100, round(cumulative_progress, 2))
            })
        
        return timeline
