
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem, Commitment, DailyTask
from app.services.inbox_service import InboxService
from app.services.commitment_service import CommitmentService
import random
from datetime import datetime, timedelta

app = create_app()

def test_auto_breakdown():
    with app.app_context():
        # Setup
        suffix = random.randint(1000, 9999)
        email = f'breakdown_{suffix}@example.com'
        user = User(name='Breakdown Test', email=email, mobile=f'555{suffix}', password_hash='hash').save()
        
        # Create Item
        item = InboxService.create_learning_item(user, {'title': 'Python Masterclass', 'source_type': 'course', 'total_duration': 600})
        
        print(f"1. Created Item: {item.title}")
        
        # Create Commitment (21 days, 5 days/week)
        # 3 weeks * 5 days = 15 days * 60m = 900m (15h) available vs 12h required -> Valid
        target_date = datetime.utcnow() + timedelta(days=21)
        
        print("2. Creating Commitment (Target: 21 days, 5 days/week)...")
        commitment = CommitmentService.create_commitment(user.id, item.id, {
            'target_completion_date': target_date,
            'daily_study_minutes': 60,
            'study_days_per_week': 5
        })
        
        # Check Tasks
        tasks = DailyTask.objects(commitment_id=commitment)
        count = tasks.count()
        print(f"✅ Generated {count} tasks.")
        
        if count == 0:
            print("❌ FAILURE: No tasks generated!")
            return

        # Check Weekend Skipping
        weekend_tasks = [t for t in tasks if t.scheduled_date.weekday() >= 5]
        if len(weekend_tasks) == 0:
             print("✅ PASSED: No tasks scheduled on weekends (as requested).")
        else:
             print(f"❌ FAILURE: Found {len(weekend_tasks)} tasks on weekends!")
             for t in weekend_tasks:
                 print(f"   - {t.scheduled_date.strftime('%A %Y-%m-%d')}")

        # Cleanup
        User.objects(email=email).delete()
        LearningItem.objects(user_id=user).delete()
        Commitment.objects(user_id=user).delete()
        DailyTask.objects(user_id=user).delete()

if __name__ == '__main__':
    test_auto_breakdown()
