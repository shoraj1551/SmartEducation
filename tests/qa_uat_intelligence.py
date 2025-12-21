
"""
QA UAT Suite - Intelligence Layer (Phase 19)
Tests features: Triggers (11), Recall (12), Pods (13), Search (15).
"""
import unittest
import json
from app import create_app
from app.models import User, TriggerRule, Notification, Flashcard, LearningItem, AccountabilityPartner, DailyTask
from app.services.auth_service import AuthService

class TestIntelligenceLayer(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['MONGODB_SETTINGS'] = {
            'db': 'smart_edu_test',
            'host': 'mongomock://localhost'
        }
        self.client = self.app.test_client()
        
        
        with self.app.app_context():
            # User Setup
            User.drop_collection()
            Notification.drop_collection()
            Flashcard.drop_collection()
            LearningItem.drop_collection()
            AccountabilityPartner.drop_collection()
            DailyTask.drop_collection()
            
            self.user = User(
                email="qa@test.com", 
                name="QA Engineer",
                mobile="9998887777"
            )
            self.user.set_password("password123")
            self.user.save()
            self.token = AuthService.generate_token(self.user.id)
            self.headers = {'Authorization': f'Bearer {self.token}'}

    def test_feature_11_triggers(self):
        """Test Context-Aware Triggers"""
        print("\n[QA] Testing Feature 11: Triggers...")
        
        # 1. Force Check
        res = self.client.post('/api/triggers/check', headers=self.headers)
        self.assertEqual(res.status_code, 200)
        logs = res.json.get('logs', [])
        print(f" -> Context Check Logs: {logs}")
        
        # 2. Simulate Trigger Condition (No Tasks)
        # Verify if morning plan triggered (mocking time might be hard, relying on logic)
        # Let's manually create a notification to test API
        Notification(user_id=self.user.id, title="Test Nudge", message="Verify Me").save()
        
        # 3. Fetch Notifications
        res = self.client.get('/api/notifications', headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]['title'], "Test Nudge")
        print(" -> Notification Fetch: PASS")

    def test_feature_12_recall(self):
        """Test Active Recall Engine"""
        print("\n[QA] Testing Feature 12: Recall...")
        
        # 1. Create Learning Item
        item = LearningItem(
            user_id=self.user.id, 
            title="QA Item",
            content_type="article"
        ).save()
        
        # 2. Generate Cards (Manual)
        payload = {
            'learning_item_id': str(item.id),
            'front': "Q1",
            'back': "A1"
        }
        res = self.client.post('/api/recall/create', json=payload, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        
        # 3. Review Flow
        res = self.client.get('/api/recall/due', headers=self.headers)
        cards = res.json
        self.assertTrue(len(cards) >= 1)
        card_id = cards[0]['id']
        
        # Submit Review (Easy -> EF should increase)
        res = self.client.post('/api/recall/review', json={'card_id': card_id, 'quality': 5}, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        
        # Verify Interval Update
        card = Flashcard.objects.get(id=card_id)
        print(f" -> Card Interval: {card.interval} (Expected > 0)")
        self.assertTrue(card.interval > 0)
        print(" -> SRS Algorithm: PASS")

    def test_feature_13_pods(self):
        """Test Accountability Pods"""
        print("\n[QA] Testing Feature 13: Pods...")
        
        # 1. Send Invite
        res = self.client.post('/api/social/invite', json={'email': 'friend@test.com'}, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        
        # 2. Verify Database State
        invite = AccountabilityPartner.objects(user_id=self.user.id, partner_email='friend@test.com').first()
        self.assertIsNotNone(invite)
        self.assertEqual(invite.status, 'pending')
        print(" -> Invite Creation: PASS")
        
        # 3. Mock Partner User & Acceptance
        friend = User(
            email="friend@test.com", 
            name="Friend",
            mobile="1112223333"
        )
        friend.set_password("pass123")
        friend.save()
        with self.app.app_context():
            friend_token = AuthService.generate_token(friend.id)
        
        res = self.client.post(f'/api/social/invites/{invite.id}/accept', headers={'Authorization': f'Bearer {friend_token}'})
        self.assertEqual(res.status_code, 200)
        
        invite.reload()
        self.assertEqual(invite.status, 'active')
        print(" -> Invite Acceptance: PASS")

    def test_feature_15_search(self):
        """Test Universal Search"""
        print("\n[QA] Testing Feature 15: Search...")
        
        item = LearningItem(user_id=self.user.id, title="Python Guide", content_type="article").save()
        
        # 1. Seed Data
        DailyTask(
            user_id=self.user.id, 
            title="Buy Groceries", 
            scheduled_date="2025-01-01", 
            duration_minutes=30, 
            learning_item_id=item
        ).save()
        
        Flashcard(user_id=self.user.id, learning_item_id=item, front="What is Python?", back="A snek").save()
        
        # 2. Query
        res = self.client.get('/api/search?q=Python', headers=self.headers)
        data = res.json
        # print(f" -> Search Results: {data}")
        
        self.assertTrue(len(data['library']) > 0 or len(data['flashcards']) > 0)
        print(" -> Search Engine: PASS")

if __name__ == '__main__':
    unittest.main()
