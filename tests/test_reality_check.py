
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

def test_reality_check():
    with app.app_context():
        # Setup
        suffix = random.randint(1000, 9999)
        email = f'reality_{suffix}@example.com'
        user = User(name='Reality User', email=email, mobile=f'777{suffix}', password_hash='hash').save()
        
        # Create a HEAVY item (e.g. 50 hour course = 3000 mins)
        item = InboxService.create_learning_item(user, {
            'title': 'Heavy Course', 
            'source_type': 'course',
            'total_duration': 3000  # 50 hours
        })
        
        print(f"1. Created 'Heavy Course' (50 hours)")
        print(f"   Required with Buffer (20%): {(3000*1.2)/60} hours")
        
        # 1. Attempt UNREALISTIC Plan
        # 10 days, 30 mins/day = 300 mins (5 hours) available vs 60 hours needed
        target_bad = datetime.utcnow() + timedelta(days=10)
        
        print("\n2. Testing UNREALISTIC Plan (10 days, 30 mins/day)...")
        try:
            CommitmentService.create_commitment(user.id, item.id, {
                'target_completion_date': target_bad,
                'daily_study_minutes': 30
            })
            print("❌ FAILED: System accepted an unrealistic plan!")
        except ValueError as e:
            print(f"✅ PASSED: Rejected as expected. \n   Message: {e}")
            
        # 2. Attempt REALISTIC Plan
        # 60 days, 90 mins/day = 5400 mins (90 hours) available vs 60 hours needed
        target_good = datetime.utcnow() + timedelta(days=60)
        
        print("\n3. Testing REALISTIC Plan (60 days, 90 mins/day)...")
        try:
            c = CommitmentService.create_commitment(user.id, item.id, {
                'target_completion_date': target_good,
                'daily_study_minutes': 90
            })
            print(f"✅ PASSED: System accepted valid plan. (Commitment ID: {c.id})")
        except ValueError as e:
            print(f"❌ FAILED: System rejected a valid plan! Error: {e}")
        
        # Cleanup
        User.objects(email=email).delete()
        LearningItem.objects(user_id=user).delete()
        Commitment.objects(user_id=user).delete()

if __name__ == '__main__':
    test_reality_check()
