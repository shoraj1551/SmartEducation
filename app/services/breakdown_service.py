
"""
Auto Breakdown Service (Feature 4)
Automatically breaks down a Learning Item into Daily Tasks based on a Commitment.
"""
from datetime import datetime, timedelta
from app.models import DailyTask, Commitment, LearningItem

class AutoBreakdownService:
    @staticmethod
    def generate_daily_tasks(commitment_id):
        """
        Generate DailyTasks for a given Commitment.
        Deletes existing future tasks for this commitment to avoid duplicates.
        """
        commitment = Commitment.objects.get(id=commitment_id)
        item = commitment.learning_item_id
        user = commitment.user_id
        
        # 1. Clear existing future tasks (Re-generation logic)
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        DailyTask.objects(
            commitment_id=commitment,
            scheduled_date__gte=today,
            status='pending'
        ).delete()
        
        # 2. Planning Parameters
        start_date = today
        end_date = commitment.target_completion_date
        daily_minutes = commitment.daily_study_minutes
        study_days = commitment.study_days_per_week
        
        current_date = start_date
        task_count = 1
        generated_tasks = []
        
        # 3. Iterate and Create Tasks
        while current_date <= end_date:
            # Check if allowed day (Simple Logic: If 5 days, skip Sat/Sun)
            is_weekend = current_date.weekday() >= 5 # 5=Sat, 6=Sun
            should_skip = (study_days == 5 and is_weekend)
            
            if not should_skip:
                task = DailyTask(
                    commitment_id=commitment,
                    learning_item_id=item,
                    user_id=user,
                    title=f"Study {item.title} (Day {task_count})",
                    description=f"Focus on progress for {daily_minutes} minutes.",
                    task_type='study',
                    scheduled_date=current_date,
                    estimated_duration_minutes=daily_minutes,
                    priority_score=item.priority_score, # Inherit priority
                    status='pending',
                    difficulty_level='medium'
                )
                task.save()
                generated_tasks.append(task)
                task_count += 1
            
            current_date += timedelta(days=1)
            
        return generated_tasks
