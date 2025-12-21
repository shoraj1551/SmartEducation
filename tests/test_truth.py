
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem, Commitment, DailyTask
from app.services.reality_service import RealityService
import random
from datetime import datetime, timedelta, date

app = create_app()

def test_truth_metrics():
    with app.app_context():
        # Setup
        suffix = random.randint(1000, 9999)
        email = f'truth_{suffix}@example.com'
        user = User(name='Truth Seeker', email=email, mobile=f'444{suffix}', password_hash='hash').save()
        
        print("\n--- Testing Reality Metrics (The Truth) ---")
        
        # 1. Simulate History (Last 3 days)
        # Create Dummy Item for tasks
        dummy_item = LearningItem(
            user_id=user, title='Dummy Work', source_type='task', 
            total_duration=100, status='active'
        ).save()

        # Day 1: Worked hard (Completed task, 60 mins) -> Invested
        t1 = DailyTask(
            learning_item_id=dummy_item, user_id=user, title='Work Day', 
            scheduled_date=datetime.utcnow() - timedelta(days=2),
            status='completed',
            completed_at=datetime.utcnow() - timedelta(days=2),
            actual_duration_minutes=60,
            learning_plan_id=None, estimated_duration_minutes=60
        ).save()
        
        # Day 2: Slacked off (Completed task, 2 mins) -> Wasted
        t2 = DailyTask(
            learning_item_id=dummy_item, user_id=user, title='Slack Day', 
            scheduled_date=datetime.utcnow() - timedelta(days=1),
            status='completed',
            completed_at=datetime.utcnow() - timedelta(days=1),
            actual_duration_minutes=2,
            learning_plan_id=None, estimated_duration_minutes=60
        ).save()
        
         # Day 3 (Today): Worked (30 mins) -> Invested
        t3 = DailyTask(
            learning_item_id=dummy_item, user_id=user, title='Today Work', 
            scheduled_date=datetime.utcnow(),
            status='completed',
            completed_at=datetime.utcnow(),
            actual_duration_minutes=30,
            learning_plan_id=None, estimated_duration_minutes=60
        ).save()
        
        # 2. Create Active Commitment to Projection
        item = LearningItem(
            user_id=user, title='Big Project', source_type='course', 
            total_duration=1000, status='active'
        ).save()
        
        comm = Commitment(
            user_id=user, learning_item_id=item,
            target_completion_date=datetime.utcnow() + timedelta(days=10),
            daily_study_minutes=100,
            status='active'
        ).save()
        
        # 3. Calculate Truth
        metrics = RealityService.calculate_truth_metrics(user.id)
        
        print(f"Days Wasted: {metrics['days_wasted']} (Expected >= 1)")
        print(f"Days Invested: {metrics['days_invested']} (Expected >= 2)")
        
        # Velocity logic: Total mins in ~7 days window = 60+2+30 = 92 mins / 7 = ~13 mins/day
        print(f"Actual Velocity: {metrics['actual_velocity']} min/day")
        
        # Projection
        if metrics['projections']:
            proj = metrics['projections'][0]
            print(f"Projected Gap: {proj['gap_days']} days late")
            # 1000 mins + 20% buffer = 1200 mins needed.
            # Velocity ~13 mins/day.
            # Days needed = 1200 / 13 = ~92 days.
            # Target = 10 days away. 
            # Gap = ~82 days late.
        else:
            print("❌ No projections found!")

        # Cleanup
        User.objects(email=email).delete()
        DailyTask.objects(user_id=user).delete()
        Commitment.objects(user_id=user).delete()
        LearningItem.objects(user_id=user).delete()

if __name__ == '__main__':
    test_truth_metrics()
