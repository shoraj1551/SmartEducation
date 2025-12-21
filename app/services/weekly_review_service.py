"""
Weekly Review Service for Feature 8: Weekly Review Assistant
Generates weekly learning reviews and insights
"""
from datetime import datetime, timedelta
from app.models import LearningItem, DailyTask, FocusSession, CommitmentViolation, User
from mongoengine.errors import DoesNotExist


class WeeklyReviewService:
    """Service for generating weekly learning reviews"""
    
    @staticmethod
    def generate_weekly_review(user_id, week_offset=0):
        """
        Generate comprehensive weekly review
        
        Args:
            user_id: User ID
            week_offset: 0 for current week, -1 for last week, etc.
            
        Returns:
            Dictionary with weekly review data
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Calculate week boundaries
        today = datetime.utcnow()
        week_start = today - timedelta(days=today.weekday() + (7 * abs(week_offset)))
        week_end = week_start + timedelta(days=7)
        
        # Collect all metrics
        stats = WeeklyReviewService._collect_weekly_stats(user, week_start, week_end)
        insights = WeeklyReviewService._generate_insights(user, stats, week_start, week_end)
        action_items = WeeklyReviewService._generate_action_items(stats, insights)
        
        return {
            'week_start': week_start.date().isoformat(),
            'week_end': week_end.date().isoformat(),
            'statistics': stats,
            'insights': insights,
            'action_items': action_items,
            'overall_grade': WeeklyReviewService._calculate_weekly_grade(stats)
        }
    
    @staticmethod
    def _collect_weekly_stats(user, week_start, week_end):
        """Collect all statistics for the week"""
        
        # Tasks completed
        completed_tasks = DailyTask.objects(
            user_id=user,
            status='completed',
            completed_at__gte=week_start,
            completed_at__lt=week_end
        )
        
        # Focus sessions
        focus_sessions = FocusSession.objects(
            user_id=user,
            started_at__gte=week_start,
            started_at__lt=week_end
        )
        
        # Commitment violations
        violations = CommitmentViolation.objects(
            user_id=user,
            violation_date__gte=week_start,
            violation_date__lt=week_end
        )
        
        # Learning items progress
        active_items = LearningItem.objects(user_id=user, status='active')
        
        # Calculate metrics
        total_tasks = completed_tasks.count()
        total_focus_time = sum(s.duration_minutes for s in focus_sessions)
        total_violations = violations.count()
        
        # Calculate average daily tasks
        days_in_week = 7
        avg_daily_tasks = total_tasks / days_in_week
        
        # Calculate completion rate
        scheduled_tasks = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=week_start.date(),
            scheduled_date__lt=week_end.date()
        ).count()
        
        completion_rate = (total_tasks / scheduled_tasks * 100) if scheduled_tasks > 0 else 0
        
        # Most productive day
        daily_breakdown = {}
        for task in completed_tasks:
            day = task.completed_at.strftime('%A')
            daily_breakdown[day] = daily_breakdown.get(day, 0) + 1
        
        most_productive_day = max(daily_breakdown.items(), key=lambda x: x[1])[0] if daily_breakdown else 'None'
        
        return {
            'tasks_completed': total_tasks,
            'tasks_scheduled': scheduled_tasks,
            'completion_rate': round(completion_rate, 2),
            'focus_time_minutes': total_focus_time,
            'focus_sessions': focus_sessions.count(),
            'commitment_violations': total_violations,
            'active_learning_items': active_items.count(),
            'avg_daily_tasks': round(avg_daily_tasks, 2),
            'most_productive_day': most_productive_day,
            'daily_breakdown': daily_breakdown
        }
    
    @staticmethod
    def _generate_insights(user, stats, week_start, week_end):
        """Generate insights from weekly data"""
        insights = []
        
        # Completion rate insight
        if stats['completion_rate'] >= 80:
            insights.append({
                'type': 'positive',
                'category': 'completion',
                'message': f"🎉 Excellent! {stats['completion_rate']}% task completion rate.",
                'icon': '🎉'
            })
        elif stats['completion_rate'] >= 60:
            insights.append({
                'type': 'neutral',
                'category': 'completion',
                'message': f"📊 Good progress at {stats['completion_rate']}% completion. Room to improve!",
                'icon': '📊'
            })
        else:
            insights.append({
                'type': 'negative',
                'category': 'completion',
                'message': f"⚠️ Only {stats['completion_rate']}% completion rate. Need to refocus!",
                'icon': '⚠️'
            })
        
        # Focus time insight
        avg_daily_focus = stats['focus_time_minutes'] / 7
        if avg_daily_focus >= 60:
            insights.append({
                'type': 'positive',
                'category': 'focus',
                'message': f"💪 Great focus! Averaged {round(avg_daily_focus)} minutes/day.",
                'icon': '💪'
            })
        elif avg_daily_focus >= 30:
            insights.append({
                'type': 'neutral',
                'category': 'focus',
                'message': f"⏱️ {round(avg_daily_focus)} min/day focus time. Try for 60+ min/day!",
                'icon': '⏱️'
            })
        else:
            insights.append({
                'type': 'negative',
                'category': 'focus',
                'message': f"🔴 Low focus time: {round(avg_daily_focus)} min/day. Increase focus sessions!",
                'icon': '🔴'
            })
        
        # Violations insight
        if stats['commitment_violations'] == 0:
            insights.append({
                'type': 'positive',
                'category': 'discipline',
                'message': "✅ Perfect! No commitment violations this week.",
                'icon': '✅'
            })
        elif stats['commitment_violations'] <= 2:
            insights.append({
                'type': 'neutral',
                'category': 'discipline',
                'message': f"⚡ {stats['commitment_violations']} violations. Stay disciplined!",
                'icon': '⚡'
            })
        else:
            insights.append({
                'type': 'negative',
                'category': 'discipline',
                'message': f"🚨 {stats['commitment_violations']} violations! Review your commitments.",
                'icon': '🚨'
            })
        
        # Productivity pattern
        if stats['most_productive_day'] != 'None':
            insights.append({
                'type': 'info',
                'category': 'pattern',
                'message': f"📅 Most productive on {stats['most_productive_day']}s. Schedule important tasks then!",
                'icon': '📅'
            })
        
        return insights
    
    @staticmethod
    def _generate_action_items(stats, insights):
        """Generate actionable recommendations"""
        actions = []
        
        # Based on completion rate
        if stats['completion_rate'] < 70:
            actions.append({
                'priority': 'high',
                'action': 'Reduce active learning items or increase daily study time',
                'reason': 'Low completion rate indicates overcommitment'
            })
        
        # Based on focus time
        if stats['focus_time_minutes'] < 210:  # Less than 30 min/day average
            actions.append({
                'priority': 'high',
                'action': 'Schedule at least 1 focus session daily (30+ minutes)',
                'reason': 'Low focus time impacts learning effectiveness'
            })
        
        # Based on violations
        if stats['commitment_violations'] > 3:
            actions.append({
                'priority': 'critical',
                'action': 'Review and adjust commitments to realistic levels',
                'reason': 'Multiple violations indicate unrealistic commitments'
            })
        
        # Based on task distribution
        if stats['avg_daily_tasks'] < 1:
            actions.append({
                'priority': 'medium',
                'action': 'Increase daily task targets or break down learning items better',
                'reason': 'Low daily task completion suggests poor planning'
            })
        
        return actions
    
    @staticmethod
    def _calculate_weekly_grade(stats):
        """
        Calculate overall weekly grade (A-F)
        """
        score = 0
        
        # Completion rate (40 points)
        score += (stats['completion_rate'] / 100) * 40
        
        # Focus time (30 points) - target 420 min/week (60 min/day)
        focus_score = min(30, (stats['focus_time_minutes'] / 420) * 30)
        score += focus_score
        
        # Discipline (20 points) - penalize violations
        discipline_score = max(0, 20 - (stats['commitment_violations'] * 5))
        score += discipline_score
        
        # Consistency (10 points) - based on daily breakdown
        if stats['avg_daily_tasks'] >= 1:
            score += 10
        elif stats['avg_daily_tasks'] >= 0.5:
            score += 5
        
        # Convert to letter grade
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def get_review_history(user_id, weeks=4):
        """Get review history for comparison"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        history = []
        for week_offset in range(weeks):
            review = WeeklyReviewService.generate_weekly_review(user_id, -week_offset)
            history.append({
                'week': f"Week of {review['week_start']}",
                'grade': review['overall_grade'],
                'completion_rate': review['statistics']['completion_rate'],
                'focus_time': review['statistics']['focus_time_minutes']
            })
        
        return history
