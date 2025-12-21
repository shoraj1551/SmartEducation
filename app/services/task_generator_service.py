"""
Task Generator Service for Feature 2: Auto Course Breakdown
Handles intelligent task generation and scheduling
"""
from datetime import datetime, timedelta
from app.models import LearningItem, LearningPlan, DailyTask, User
from mongoengine.errors import DoesNotExist
import math


class TaskGeneratorService:
    """Service for generating daily tasks from learning items"""
    
    # Default settings
    DEFAULT_BUFFER_PERCENTAGE = 20.0
    MIN_TASK_DURATION = 15  # Minimum 15 minutes per task
    MAX_TASK_DURATION = 120  # Maximum 2 hours per task
    OPTIMAL_TASK_DURATION = 45  # Optimal 45 minutes per task
    
    @staticmethod
    def generate_learning_plan(learning_item_id, user_id, plan_config):
        """
        Generate a complete learning plan with daily tasks
        
        Args:
            learning_item_id: ID of the learning item
            user_id: User ID
            plan_config: Dictionary with:
                - target_completion_date: datetime
                - daily_availability_minutes: int
                - skip_weekends: bool (optional)
                - buffer_percentage: float (optional)
                
        Returns:
            LearningPlan object with generated tasks
        """
        # Get learning item
        try:
            item = LearningItem.objects.get(id=learning_item_id)
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("Learning item or user not found")
        
        # Validate configuration
        if 'target_completion_date' not in plan_config:
            raise ValueError("target_completion_date is required")
        if 'daily_availability_minutes' not in plan_config:
            raise ValueError("daily_availability_minutes is required")
        
        target_date = plan_config['target_completion_date']
        daily_minutes = plan_config['daily_availability_minutes']
        skip_weekends = plan_config.get('skip_weekends', True)
        buffer_pct = plan_config.get('buffer_percentage', TaskGeneratorService.DEFAULT_BUFFER_PERCENTAGE)
        
        # Calculate total duration with buffer
        base_duration = item.total_duration
        buffered_duration = base_duration * (1 + buffer_pct / 100)
        
        # Create learning plan
        plan = LearningPlan(
            learning_item_id=item,
            user_id=user,
            target_completion_date=target_date,
            daily_availability_minutes=daily_minutes,
            total_estimated_duration=int(buffered_duration),
            skip_weekends=skip_weekends,
            buffer_percentage=buffer_pct,
            plan_metadata={
                'original_duration': base_duration,
                'buffer_added': int(buffered_duration - base_duration)
            }
        )
        plan.save()
        
        # Generate tasks
        tasks = TaskGeneratorService._generate_tasks(plan, item)
        plan.total_tasks = len(tasks)
        plan.save()
        
        return plan
    
    @staticmethod
    def _generate_tasks(plan, item):
        """Generate individual daily tasks for a plan"""
        tasks = []
        
        # Calculate available study days
        start_date = datetime.utcnow()
        end_date = plan.target_completion_date
        study_days = TaskGeneratorService._calculate_study_days(
            start_date, end_date, plan.skip_weekends
        )
        
        if len(study_days) == 0:
            raise ValueError("No available study days between now and target date")
        
        # Calculate task breakdown
        total_duration = plan.total_estimated_duration
        daily_minutes = plan.daily_availability_minutes
        
        # Determine number of tasks per day and duration
        tasks_breakdown = TaskGeneratorService._calculate_task_breakdown(
            total_duration, daily_minutes, len(study_days)
        )
        
        # Generate tasks
        task_index = 0
        for day_index, study_date in enumerate(study_days):
            day_tasks = tasks_breakdown.get(day_index, [])
            
            for task_duration in day_tasks:
                task_index += 1
                
                # Determine task type and difficulty
                progress_pct = (task_index / sum(len(v) for v in tasks_breakdown.values())) * 100
                difficulty = TaskGeneratorService._estimate_difficulty(progress_pct)
                task_type = TaskGeneratorService._determine_task_type(task_index, progress_pct)
                
                # Create task
                task = DailyTask(
                    learning_plan_id=plan,
                    learning_item_id=item,
                    user_id=plan.user_id,
                    title=f"{item.title} - Day {day_index + 1}, Task {len(day_tasks)}",
                    description=f"Study session {task_index}",
                    task_type=task_type,
                    scheduled_date=study_date,
                    estimated_duration_minutes=task_duration,
                    difficulty_level=difficulty,
                    priority_score=TaskGeneratorService._calculate_priority(day_index, len(study_days)),
                    content_reference={
                        'task_number': task_index,
                        'day_number': day_index + 1,
                        'progress_percentage': progress_pct
                    }
                )
                
                # Add dependencies (sequential learning)
                if task_index > 1:
                    task.depends_on_task_ids = [str(tasks[-1].id)]
                
                task.save()
                tasks.append(task)
        
        return tasks
    
    @staticmethod
    def _calculate_study_days(start_date, end_date, skip_weekends):
        """Calculate available study days between start and end date"""
        study_days = []
        current_date = start_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        while current_date <= end_date:
            # Skip weekends if configured
            if skip_weekends and current_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                current_date += timedelta(days=1)
                continue
            
            study_days.append(current_date)
            current_date += timedelta(days=1)
        
        return study_days
    
    @staticmethod
    def _calculate_task_breakdown(total_duration, daily_minutes, num_days):
        """
        Calculate how to break down total duration into daily tasks
        
        Returns:
            Dictionary mapping day_index to list of task durations
        """
        breakdown = {}
        remaining_duration = total_duration
        
        for day_index in range(num_days):
            if remaining_duration <= 0:
                break
            
            # Determine how much time to allocate for this day
            day_allocation = min(daily_minutes, remaining_duration)
            
            # Break day allocation into optimal task chunks
            day_tasks = []
            day_remaining = day_allocation
            
            while day_remaining > 0:
                # Prefer optimal task duration, but adjust based on remaining time
                if day_remaining >= TaskGeneratorService.OPTIMAL_TASK_DURATION:
                    task_duration = TaskGeneratorService.OPTIMAL_TASK_DURATION
                elif day_remaining >= TaskGeneratorService.MIN_TASK_DURATION:
                    task_duration = day_remaining
                else:
                    # Merge small remaining time with previous task
                    if day_tasks:
                        day_tasks[-1] += day_remaining
                    break
                
                day_tasks.append(task_duration)
                day_remaining -= task_duration
            
            if day_tasks:
                breakdown[day_index] = day_tasks
                remaining_duration -= sum(day_tasks)
        
        return breakdown
    
    @staticmethod
    def _estimate_difficulty(progress_percentage):
        """Estimate task difficulty based on course progress"""
        if progress_percentage < 20:
            return 'easy'  # Introduction phase
        elif progress_percentage < 70:
            return 'medium'  # Main content
        else:
            return 'hard'  # Advanced/final topics
    
    @staticmethod
    def _determine_task_type(task_index, progress_percentage):
        """Determine task type based on position in course"""
        if task_index == 1:
            return 'introduction'
        elif progress_percentage > 90:
            return 'review'
        elif progress_percentage > 80:
            return 'project'
        else:
            return 'study'
    
    @staticmethod
    def _calculate_priority(day_index, total_days):
        """Calculate priority score (higher for earlier tasks and near deadline)"""
        # Priority increases as we get closer to deadline
        urgency_score = (total_days - day_index) / total_days
        return urgency_score * 100
    
    @staticmethod
    def get_today_tasks(user_id):
        """Get all tasks scheduled for today"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        today = datetime.utcnow().date()
        
        tasks = DailyTask.objects(
            user_id=user,
            scheduled_date__gte=datetime(today.year, today.month, today.day),
            scheduled_date__lt=datetime(today.year, today.month, today.day) + timedelta(days=1),
            status__in=['pending', 'in_progress']
        ).order_by('priority_score', 'scheduled_date')
        
        return list(tasks)
    
    @staticmethod
    def complete_task(task_id, actual_duration=None):
        """Mark a task as completed"""
        try:
            task = DailyTask.objects.get(id=task_id)
            task.mark_complete(actual_duration)
            
            # Update learning item progress
            item = task.learning_item_id
            if actual_duration:
                item.completed_duration += actual_duration
            else:
                item.completed_duration += task.estimated_duration_minutes
            item.update_progress()
            
            return task
        except DoesNotExist:
            raise ValueError("Task not found")
    
    @staticmethod
    def reschedule_plan(plan_id, new_target_date=None, new_daily_minutes=None):
        """
        Reschedule a learning plan (adaptive rescheduling)
        
        Args:
            plan_id: Learning plan ID
            new_target_date: New target completion date (optional)
            new_daily_minutes: New daily availability (optional)
            
        Returns:
            Updated plan with rescheduled tasks
        """
        try:
            plan = LearningPlan.objects.get(id=plan_id)
        except DoesNotExist:
            raise ValueError("Learning plan not found")
        
        # Delete incomplete tasks
        DailyTask.objects(
            learning_plan_id=plan,
            status__in=['pending', 'in_progress']
        ).delete()
        
        # Update plan configuration
        if new_target_date:
            plan.target_completion_date = new_target_date
        if new_daily_minutes:
            plan.daily_availability_minutes = new_daily_minutes
        
        # Calculate remaining duration
        item = plan.learning_item_id
        remaining_duration = item.total_duration - item.completed_duration
        plan.total_estimated_duration = int(remaining_duration * (1 + plan.buffer_percentage / 100))
        
        plan.last_adjusted_at = datetime.utcnow()
        plan.save()
        
        # Regenerate tasks for remaining work
        new_tasks = TaskGeneratorService._generate_tasks(plan, item)
        plan.total_tasks = plan.completed_tasks + len(new_tasks)
        plan.save()
        
        return plan
