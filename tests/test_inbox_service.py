"""
Unit tests for InboxService
Tests CRUD operations, validation logic, and business rules
"""
import unittest
from datetime import datetime, timedelta
from mongoengine import connect, disconnect
from models import User, LearningItem
from services.inbox_service import InboxService


class TestInboxService(unittest.TestCase):
    """Test cases for InboxService"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database connection"""
        connect('mongoenginetest', host='mongomock://localhost')
    
    @classmethod
    def tearDownClass(cls):
        """Disconnect from test database"""
        disconnect()
    
    def setUp(self):
        """Set up test data before each test"""
        # Clear collections
        User.drop_collection()
        LearningItem.drop_collection()
        
        # Create test user
        self.test_user = User(
            name="Test User",
            email="test@example.com",
            mobile="1234567890",
            password_hash="hashed_password"
        )
        self.test_user.save()
    
    def tearDown(self):
        """Clean up after each test"""
        User.drop_collection()
        LearningItem.drop_collection()
    
    def test_create_learning_item_success(self):
        """Test successful creation of a learning item"""
        item_data = {
            'title': 'Python for Beginners',
            'source_type': 'course',
            'description': 'Learn Python basics',
            'platform': 'udemy',
            'total_duration': 600
        }
        
        item = InboxService.create_learning_item(self.test_user.id, item_data)
        
        self.assertIsNotNone(item)
        self.assertEqual(item.title, 'Python for Beginners')
        self.assertEqual(item.source_type, 'course')
        self.assertEqual(item.status, 'active')
        self.assertEqual(item.total_duration, 600)
    
    def test_create_item_missing_required_field(self):
        """Test creation fails with missing required field"""
        item_data = {
            'description': 'Missing title'
        }
        
        with self.assertRaises(ValueError) as context:
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        self.assertIn('Missing required field', str(context.exception))
    
    def test_create_item_invalid_source_type(self):
        """Test creation fails with invalid source type"""
        item_data = {
            'title': 'Test Item',
            'source_type': 'invalid_type'
        }
        
        with self.assertRaises(ValueError) as context:
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        self.assertIn('Invalid source_type', str(context.exception))
    
    def test_max_active_items_limit(self):
        """Test that max active items limit is enforced"""
        # Create 3 active items (max limit)
        for i in range(3):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Try to create 4th active item
        item_data = {
            'title': 'Course 4',
            'source_type': 'course'
        }
        
        with self.assertRaises(ValueError) as context:
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        self.assertIn('Cannot add new item', str(context.exception))
        self.assertIn('3 active items', str(context.exception))
    
    def test_get_user_items(self):
        """Test retrieving user items"""
        # Create multiple items with different statuses
        for i, status in enumerate(['active', 'paused', 'completed']):
            item_data = {
                'title': f'Item {i+1}',
                'source_type': 'course'
            }
            item = InboxService.create_learning_item(self.test_user.id, item_data)
            if status != 'active':
                InboxService.update_item_status(item.id, status, self.test_user.id)
        
        # Get all items
        all_items = InboxService.get_user_items(self.test_user.id)
        self.assertEqual(len(all_items), 3)
        
        # Get only active items
        active_items = InboxService.get_user_items(self.test_user.id, status_filter='active')
        self.assertEqual(len(active_items), 1)
        
        # Get only paused items
        paused_items = InboxService.get_user_items(self.test_user.id, status_filter='paused')
        self.assertEqual(len(paused_items), 1)
    
    def test_update_item_status(self):
        """Test updating item status"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'course'
        }
        item = InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Update to paused
        updated_item = InboxService.update_item_status(item.id, 'paused', self.test_user.id)
        self.assertEqual(updated_item.status, 'paused')
        self.assertIsNotNone(updated_item.paused_at)
        
        # Update to completed
        updated_item = InboxService.update_item_status(item.id, 'completed', self.test_user.id)
        self.assertEqual(updated_item.status, 'completed')
        self.assertIsNotNone(updated_item.completed_at)
        self.assertEqual(updated_item.progress_percentage, 100.0)
    
    def test_update_status_invalid(self):
        """Test updating to invalid status fails"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'course'
        }
        item = InboxService.create_learning_item(self.test_user.id, item_data)
        
        with self.assertRaises(ValueError) as context:
            InboxService.update_item_status(item.id, 'invalid_status', self.test_user.id)
        
        self.assertIn('Invalid status', str(context.exception))
    
    def test_update_progress(self):
        """Test updating item progress"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'course',
            'total_duration': 100
        }
        item = InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Update progress to 50%
        updated_item = InboxService.update_progress(item.id, 50, self.test_user.id)
        self.assertEqual(updated_item.completed_duration, 50)
        self.assertEqual(updated_item.progress_percentage, 50.0)
        self.assertIsNotNone(updated_item.last_accessed_at)
        
        # Update progress to 100% (should auto-complete)
        updated_item = InboxService.update_progress(item.id, 100, self.test_user.id)
        self.assertEqual(updated_item.progress_percentage, 100.0)
        self.assertEqual(updated_item.status, 'completed')
        self.assertIsNotNone(updated_item.completed_at)
    
    def test_delete_item(self):
        """Test deleting an item"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'course'
        }
        item = InboxService.create_learning_item(self.test_user.id, item_data)
        item_id = item.id
        
        # Delete item
        result = InboxService.delete_item(item_id, self.test_user.id)
        self.assertTrue(result)
        
        # Verify item is deleted
        deleted_item = InboxService.get_item_by_id(item_id, self.test_user.id)
        self.assertIsNone(deleted_item)
    
    def test_get_inbox_stats(self):
        """Test getting inbox statistics"""
        # Create items with different statuses
        statuses = ['active', 'active', 'paused', 'completed', 'dropped']
        for i, status in enumerate(statuses):
            item_data = {
                'title': f'Item {i+1}',
                'source_type': 'course',
                'total_duration': 100
            }
            item = InboxService.create_learning_item(self.test_user.id, item_data)
            if status != 'active':
                InboxService.update_item_status(item.id, status, self.test_user.id)
            
            # Add some completed duration
            InboxService.update_progress(item.id, 20, self.test_user.id)
        
        stats = InboxService.get_inbox_stats(self.test_user.id)
        
        self.assertEqual(stats['total_items'], 5)
        self.assertEqual(stats['active_items'], 2)
        self.assertEqual(stats['paused_items'], 1)
        self.assertEqual(stats['completed_items'], 1)
        self.assertEqual(stats['dropped_items'], 1)
        self.assertEqual(stats['total_time_invested_minutes'], 100)  # 5 items × 20 minutes
        self.assertTrue(stats['can_add_new_item'])  # Only 2 active, can add 1 more
        self.assertEqual(stats['slots_available'], 1)
    
    def test_bulk_update_status(self):
        """Test bulk status update"""
        # Create 3 items
        item_ids = []
        for i in range(3):
            item_data = {
                'title': f'Item {i+1}',
                'source_type': 'course'
            }
            item = InboxService.create_learning_item(self.test_user.id, item_data)
            item_ids.append(str(item.id))
        
        # Bulk update to paused
        result = InboxService.bulk_update_status(item_ids, 'paused', self.test_user.id)
        
        self.assertEqual(len(result['updated_items']), 3)
        self.assertEqual(len(result['errors']), 0)
        
        # Verify all items are paused
        for item_id in item_ids:
            item = InboxService.get_item_by_id(item_id, self.test_user.id)
            self.assertEqual(item.status, 'paused')


if __name__ == '__main__':
    unittest.main()
