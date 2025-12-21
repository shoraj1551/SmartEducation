
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem
from app.services.priority_service import PriorityService
import random
from datetime import datetime, timedelta

app = create_app()

def test_priority_algo():
    with app.app_context():
        # Setup
        suffix = random.randint(1000, 9999)
        email = f'priority_{suffix}@example.com'
        user = User(name='Priority User', email=email, mobile=f'666{suffix}', password_hash='hash').save()
        
        print("\n--- Testing Priority Algorithm ---")
        
        # 1. Urgent & Important (Due tomorrow, High Relevance)
        item1 = LearningItem(
            user_id=user,
            title='Urgent Task',
            source_type='task',
            priority_score=0.9, # Relevance
            target_completion_date=datetime.utcnow() + timedelta(days=1),
            total_duration=120,
            status='active'
        ).save()
        
        score1 = PriorityService.calculate_score(item1)
        print(f"1. Urgent Item Score: {score1} (Expected > 75)")
        # relevance(.9*40=36) + urgency(.9*40=36) + effort(10) = 82
        
        # 2. Long Term & Low Relevance (Due 60 days, Low Relevance)
        item2 = LearningItem(
            user_id=user,
            title='Someday Task',
            source_type='task',
            priority_score=0.3, # Relevance
            target_completion_date=datetime.utcnow() + timedelta(days=60),
            total_duration=300,
            status='active'
        ).save()
        
        score2 = PriorityService.calculate_score(item2)
        print(f"2. Long Term Item Score: {score2} (Expected < 50)")
        # relevance(.3*40=12) + urgency(.2*40=8) + effort(5) = 25
        
        # 3. Quick Win (No deadline, High Relevance, Short)
        item3 = LearningItem(
            user_id=user,
            title='Quick Win',
            source_type='video',
            priority_score=0.8,
            total_duration=15, # 15 mins
            status='active'
        ).save()
        
        score3 = PriorityService.calculate_score(item3)
        print(f"3. Quick Win Score: {score3} (Expected ~50-60)")
        # relevance(.8*40=32) + urgency(0) + effort(20) = 52
        
        # Cleanup
        User.objects(email=email).delete()
        LearningItem.objects(user_id=user).delete()

if __name__ == '__main__':
    test_priority_algo()
