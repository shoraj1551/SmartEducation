
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem, Commitment
from app.services.inbox_service import InboxService
from app.services.commitment_service import CommitmentService
import random
from datetime import datetime, timedelta

app = create_app()

def test_commitment_logic():
    with app.app_context():
        # Setup
        suffix = random.randint(1000, 9999)
        email = f'commit_{suffix}@example.com'
        user = User(name='Commit Test', email=email, mobile=f'888{suffix}', password_hash='hash').save()
        
        # Create an item
        item = InboxService.create_learning_item(user, {'title': 'Hard Course', 'source_type': 'video'})
        
        print(f"1. Created User and Item: {item.title}")
        
        # 1. Create Commitment
        target_date = datetime.utcnow() + timedelta(days=30)
        commitment = CommitmentService.create_commitment(user.id, item.id, {
            'target_completion_date': target_date,
            'daily_study_minutes': 60
        })
        print(f"✅ Step 1: Commitment Created (Locked: {commitment.is_locked})")
        
        # 2. Modify (First Time) - Should Succeed
        commitment = CommitmentService.modify_commitment(commitment.id, {'daily_study_minutes': 45})
        print(f"✅ Step 2: Modified successfully (Count: {commitment.modification_count})")
        
        # 3. Modify (Second Time) - Should Succeed
        commitment = CommitmentService.modify_commitment(commitment.id, {'daily_study_minutes': 30})
        print(f"✅ Step 3: Modified successfully (Count: {commitment.modification_count})")
        
        # 4. Modify (Third Time) - Should Fail
        try:
            CommitmentService.modify_commitment(commitment.id, {'daily_study_minutes': 15})
            print("❌ Step 4 FAILED: Allowed 3rd modification!")
        except ValueError as e:
            print(f"✅ Step 4: Blocked 3rd modification. Error: {e}")
            
        # 5. Daily Check-In
        commitment = CommitmentService.daily_check_in(commitment.id, 45) # Exceeds 30
        print(f"✅ Step 5: Check-in successful (Streak: {commitment.current_streak})")
        
        # Cleanup
        User.objects(email=email).delete()
        LearningItem.objects(user_id=user).delete()
        Commitment.objects(user_id=user).delete()

if __name__ == '__main__':
    test_commitment_logic()
