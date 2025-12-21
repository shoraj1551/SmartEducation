
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, LearningItem
from app.services.inbox_service import InboxService
import random

app = create_app()

def test_status_transitions():
    with app.app_context():
        # Setup Unique User
        suffix = random.randint(10000, 99999)
        email = f'flow_test_{suffix}@example.com'
        mobile = f'99999{suffix}'
        
        user = User(
            name='Flow Test User',
            email=email,
            mobile=mobile,
            password_hash='hash'
        ).save()
        
        print(f"User created: {email}")
        
        # 1. Fill Capacity (3 Items)
        items = []
        for i in range(3):
            item = InboxService.create_learning_item(user, {
                'title': f'Item {i}',
                'source_type': 'video'
            })
            items.append(item)
        print("✅ Step 1: Created 3 active items.")
        
        # 2. Try adding 4th (Should Fail)
        try:
            InboxService.create_learning_item(user, {'title': 'Item 4', 'source_type': 'video'})
            print("❌ Step 2 FAILED: Allowed 4th item!")
        except ValueError:
            print("✅ Step 2: Correctly blocked 4th item.")
            
        # 3. Pause Item 1 (Free up slot)
        InboxService.update_item_status(items[0].id, 'paused', user.id)
        print(f"✅ Step 3: Paused Item 0 ({items[0].title}).")
        
        # 4. Add new item (Should Succeed now)
        try:
            item4 = InboxService.create_learning_item(user, {'title': 'Item 4', 'source_type': 'video'})
            print("✅ Step 4: Successfully added Item 4 (Slot was available).")
        except ValueError as e:
            print(f"❌ Step 4 FAILED: Could not add item even after pausing: {e}")
            
        # 5. Try Unpausing Item 1 (Should Fail - Capacity Full again)
        try:
            InboxService.update_item_status(items[0].id, 'active', user.id)
            print("❌ Step 5 FAILED: Allowed unpausing when full!")
        except ValueError as e:
            print("✅ Step 5: Correctly blocked unpausing (Capacity Full).")
            
        # 6. Complete Item 2
        InboxService.update_item_status(items[1].id, 'completed', user.id)
        print("✅ Step 6: Completed Item 1.")
        
        # 7. Unpause Item 1 (Should Succeed now)
        try:
            InboxService.update_item_status(items[0].id, 'active', user.id)
            print("✅ Step 7: Successfully unpaused Item 0.")
        except ValueError as e:
            print(f"❌ Step 7 FAILED: Could not unpause: {e}")

        # Cleanup
        User.objects(email=email).delete()
        LearningItem.objects(user_id=user).delete()

if __name__ == '__main__':
    test_status_transitions()
