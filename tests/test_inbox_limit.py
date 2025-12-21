
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem
from app.services.inbox_service import InboxService
import mongoengine

app = create_app()

def test_blocking_logic():
    with app.app_context():
        import random
        suffix = random.randint(1000, 9999)
        unique_mobile = f'123456{suffix}'
        
        # Cleanup potential existing
        User.objects(email='test_block@example.com').delete()
        User.objects(mobile=unique_mobile).delete()

        user = User(
            name='Test User',
            email='test_block@example.com',
            mobile=unique_mobile,
            password_hash='hash'
        ).save()
        
        LearningItem.objects(user_id=user).delete()
        
        print("1. Creating 3 Active Items...")
        for i in range(3):
            InboxService.create_learning_item(user, {
                'title': f'Item {i}',
                'source_type': 'video'
            })
            print(f"   Created Item {i}")
            
        print("\n2. Attempting to create 4th item (Should Fail)...")
        try:
            InboxService.create_learning_item(user, {
                'title': 'Item 4',
                'source_type': 'video'
            })
            print("❌ FAILED: Item 4 was created (Blocking logic missing!)")
        except ValueError as e:
            print(f"✅ PASSED: Blocked with message: {e}")
            
        print("\n3. Testing 'Check Capacity'...")
        check = InboxService.check_can_add_item(user)
        if not check['can_add']:
             print(f"✅ PASSED: check_can_add_item returned False. Reason: {check.get('reason')}")
        else:
             print("❌ FAILED: check_can_add_item returned True")

        # Cleanup
        User.objects(email='test_block@example.com').delete()
        LearningItem.objects(user_id=user).delete()

if __name__ == '__main__':
    test_blocking_logic()
