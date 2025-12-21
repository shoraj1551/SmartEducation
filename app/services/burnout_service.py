"""
Burnout Detection Service for Feature 9: Burnout-Aware Adaptive Scheduling
Detects burnout patterns and provides adaptive scheduling
"""
from datetime import datetime, timedelta
from app.models import DailyTask, FocusSession, LearningItem, User, LearningPlan
from mongoengine.errors import DoesNotExist


class BurnoutDetectionService:
    """Service for detecting burnout and adapting schedules"""
    
    # Burnout thresholds
    BURNOUT_SCORE_CRITICAL = 70
    BURNOUT_SCORE_WARNING = 50
    
    @staticmethod
    def calculate_burnout_score(user_id, days=14):
        """
        Calculate burnout score (0-100)
        Higher score = higher burnout risk
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary with burnout score and factors
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Calculate individual factors
        missed_sessions_score = BurnoutDetectionService._analyze_missed_sessions(user, since_date)
        completion_trend_score = BurnoutDetectionService._analyze_completion_trend(user, since_date)
        delay_score = BurnoutDetectionService._analyze_session_delays(user, since_date)
        overwork_score = BurnoutDetectionService._analyze_overwork_pattern(user, since_date)
        
        # Weighted burnout score
        burnout_score = (
            missed_sessions_score * 0.30 +
            completion_trend_score * 0.25 +
            delay_score * 0.20 +
            overwork_score * 0.25
        )
        
        # Determine risk level
        if burnout_score >= BurnoutDetectionService.BURNOUT_SCORE_CRITICAL:
            risk_level = 'critical'
            message = '🚨 Critical burnout risk! Immediate action needed.'
        elif burnout_score >= BurnoutDetectionService.BURNOUT_SCORE_WARNING:
            risk_level = 'warning'
            message = '⚠️ Burnout warning. Consider reducing workload.'
        else:
            risk_level = 'healthy'
            message = '✅ Healthy learning pace. Keep it up!'
        
        return {
            'burnout_score': round(burnout_score, 2),
            'risk_level': risk_level,
            'message': message,
            'factors': {
                'missed_sessions': round(missed_sessions_score, 2),
                'completion_trend': round(completion_trend_score, 2),
                'session_delays': round(delay_score, 2),
                'overwork_pattern': round(overwork_score, 2)
            }
        }
    
    @staticmethod
    def _analyze_missed_sessions(user, since_date):
        """Analyze missed session patterns (0-100)"""
        scheduled_tasks = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=since_date.date(),
            scheduled_date__lt=datetime.utcnow().date()
        )
        
        total_scheduled = scheduled_tasks.count()
        if total_scheduled == 0:
            return 0
        
        missed_tasks = scheduled_tasks.filter(status__ne='completed').count()
        miss_rate = (missed_tasks / total_scheduled) * 100
        
        # Score increases with miss rate
        return min(100, miss_rate * 1.5)
    
    @staticmethod
    def _analyze_completion_trend(user, since_date):
        """Analyze completion rate trend (0-100)"""
        # Split period into two halves
        mid_date = since_date + timedelta(days=7)
        
        # First half completion rate
        first_half_scheduled = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=since_date.date(),
            scheduled_date__lt=mid_date.date()
        ).count()
        
        first_half_completed = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=since_date.date(),
            scheduled_date__lt=mid_date.date(),
            status='completed'
        ).count()
        
        # Second half completion rate
        second_half_scheduled = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=mid_date.date(),
            scheduled_date__lt=datetime.utcnow().date()
        ).count()
        
        second_half_completed = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=mid_date.date(),
            scheduled_date__lt=datetime.utcnow().date(),
            status='completed'
        ).count()
        
        # Calculate rates
        first_rate = (first_half_completed / first_half_scheduled * 100) if first_half_scheduled > 0 else 0
        second_rate = (second_half_completed / second_half_scheduled * 100) if second_half_scheduled > 0 else 0
        
        # Declining trend = higher score
        decline = first_rate - second_rate
        if decline > 0:
            return min(100, decline * 2)
        else:
            return 0
    
    @staticmethod
    def _analyze_session_delays(user, since_date):
        """Analyze session delay patterns (0-100)"""
        tasks = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=since_date.date(),
            status='completed'
        )
        
        total_delays = 0
        delayed_count = 0
        
        for task in tasks:
            if task.completed_at and task.scheduled_date:
                scheduled_datetime = datetime.combine(task.scheduled_date, datetime.min.time())
                delay_days = (task.completed_at - scheduled_datetime).days
                
                if delay_days > 0:
                    delayed_count += 1
                    total_delays += delay_days
        
        if tasks.count() == 0:
            return 0
        
        # Average delay and percentage delayed
        avg_delay = total_delays / tasks.count() if tasks.count() > 0 else 0
        delay_percentage = (delayed_count / tasks.count() * 100) if tasks.count() > 0 else 0
        
        # Score based on both metrics
        return min(100, (avg_delay * 10) + (delay_percentage * 0.5))
    
    @staticmethod
    def _analyze_overwork_pattern(user, since_date):
        """Analyze overwork patterns (0-100)"""
        focus_sessions = FocusSession.objects(
            user_id=user,
            started_at__gte=since_date
        )
        
        # Group by day
        daily_focus_time = {}
        for session in focus_sessions:
            day = session.started_at.date()
            daily_focus_time[day] = daily_focus_time.get(day, 0) + session.duration_minutes
        
        # Count days with excessive focus time (>180 min = 3 hours)
        overwork_days = sum(1 for minutes in daily_focus_time.values() if minutes > 180)
        
        # Calculate score
        total_days = len(daily_focus_time)
        if total_days == 0:
            return 0
        
        overwork_rate = (overwork_days / total_days * 100)
        return min(100, overwork_rate * 1.5)
    
    @staticmethod
    def get_adaptive_recommendations(user_id):
        """
        Get adaptive scheduling recommendations based on burnout score
        
        Returns:
            List of recommendations
        """
        burnout_data = BurnoutDetectionService.calculate_burnout_score(user_id)
        recommendations = []
        
        if burnout_data['risk_level'] == 'critical':
            recommendations.extend([
                {
                    'priority': 'critical',
                    'action': 'Take a 2-3 day break from all learning activities',
                    'reason': 'Critical burnout detected - rest is essential'
                },
                {
                    'priority': 'critical',
                    'action': 'Reduce active learning items by 50%',
                    'reason': 'Current workload is unsustainable'
                },
                {
                    'priority': 'high',
                    'action': 'Extend all target dates by 2 weeks',
                    'reason': 'Relieve deadline pressure'
                }
            ])
        elif burnout_data['risk_level'] == 'warning':
            recommendations.extend([
                {
                    'priority': 'high',
                    'action': 'Take 1 rest day this week',
                    'reason': 'Prevent burnout from escalating'
                },
                {
                    'priority': 'medium',
                    'action': 'Reduce daily study time by 25%',
                    'reason': 'Current pace is leading to burnout'
                },
                {
                    'priority': 'medium',
                    'action': 'Add buffer days to your schedule',
                    'reason': 'Reduce pressure and allow flexibility'
                }
            ])
        
        # Factor-specific recommendations
        if burnout_data['factors']['missed_sessions'] > 50:
            recommendations.append({
                'priority': 'high',
                'action': 'Review and reduce daily task targets',
                'reason': 'High miss rate indicates unrealistic planning'
            })
        
        if burnout_data['factors']['overwork_pattern'] > 50:
            recommendations.append({
                'priority': 'medium',
                'action': 'Limit daily focus sessions to 2 hours maximum',
                'reason': 'Overwork pattern detected'
            })
        
        return recommendations
    
    @staticmethod
    def apply_adaptive_schedule(plan_id):
        """
        Apply adaptive scheduling to a learning plan
        
        Args:
            plan_id: Learning plan ID
            
        Returns:
            Updated plan with adaptive adjustments
        """
        try:
            plan = LearningPlan.objects.get(id=plan_id)
        except DoesNotExist:
            raise ValueError("Learning plan not found")
        
        # Get burnout score
        burnout_data = BurnoutDetectionService.calculate_burnout_score(plan.user_id)
        
        # Apply adjustments based on burnout level
        if burnout_data['risk_level'] == 'critical':
            # Reduce daily minutes by 50%
            plan.daily_study_minutes = int(plan.daily_study_minutes * 0.5)
            # Extend target date by 2 weeks
            if plan.target_completion_date:
                plan.target_completion_date += timedelta(days=14)
            # Increase buffer
            plan.buffer_percentage = 30
        elif burnout_data['risk_level'] == 'warning':
            # Reduce daily minutes by 25%
            plan.daily_study_minutes = int(plan.daily_study_minutes * 0.75)
            # Extend target date by 1 week
            if plan.target_completion_date:
                plan.target_completion_date += timedelta(days=7)
            # Increase buffer
            plan.buffer_percentage = 25
        
        plan.save()
        return plan
