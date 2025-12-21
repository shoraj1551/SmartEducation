"""
Unit tests for Feature 1 Phase 2: Content Blocking Logic
Tests validation, capacity checks, and warning systems
"""
import unittest
from datetime import datetime
from mongoengine import connect, disconnect
from app.models import User, LearningItem
from app.services.inbox_service import InboxService


import mongomock
from app.models import User, LearningItem
from app.services.inbox_service import InboxService


class TestContentBlockingLogic(unittest.TestCase):
    """Test cases for content blocking and validation logic"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database connection"""
        connect('mongoenginetest', mongo_client_class=mongomock.MongoClient)
    
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
    
    def test_check_can_add_item_with_no_items(self):
        """Test capacity check when user has no items"""
        result = InboxService.check_can_add_item(self.test_user.id)
        
        self.assertTrue(result['can_add'])
        self.assertEqual(result['active_count'], 0)
        self.assertEqual(result['slots_available'], 3)
        self.assertIn('You can add new items', result['message'])
    
    def test_check_can_add_item_approaching_limit(self):
        """Test capacity check when approaching limit (2/3 items)"""
        # Create 2 active items
        for i in range(2):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        result = InboxService.check_can_add_item(self.test_user.id)
        
        self.assertTrue(result['can_add'])
        self.assertEqual(result['active_count'], 2)
        self.assertEqual(result['slots_available'], 1)
        self.assertIn('warning', result)
        self.assertIn('Only 1 slot remaining', result['warning'])
    
    def test_check_can_add_item_at_limit(self):
        """Test capacity check when at maximum limit"""
        # Create 3 active items (max limit)
        for i in range(3):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        result = InboxService.check_can_add_item(self.test_user.id)
        
        self.assertFalse(result['can_add'])
        self.assertEqual(result['active_count'], 3)
        self.assertEqual(result['slots_available'], 0)
        self.assertIn('reason', result)
        self.assertIn('Maximum active items limit reached', result['reason'])
        self.assertIn('suggestions', result)
        self.assertEqual(len(result['suggestions']), 3)
        self.assertIn('active_items', result)
        self.assertEqual(len(result['active_items']), 3)
    
    def test_get_blocking_details_when_not_blocked(self):
        """Test blocking details when user can add items"""
        details = InboxService.get_blocking_details(self.test_user.id)
        
        self.assertFalse(details['is_blocked'])
        self.assertIn('You can add new learning items', details['message'])
    
    def test_get_blocking_details_when_blocked(self):
        """Test blocking details when user is at limit"""
        # Create 3 items with different progress levels
        progress_levels = [80, 50, 20]
        for i, progress in enumerate(progress_levels):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course',
                'total_duration': 100
            }
            item = InboxService.create_learning_item(self.test_user.id, item_data)
            InboxService.update_progress(item.id, progress, self.test_user.id)
        
        details = InboxService.get_blocking_details(self.test_user.id)
        
        self.assertTrue(details['is_blocked'])
        self.assertEqual(details['active_count'], 3)
        self.assertIn('active_items_details', details)
        self.assertEqual(len(details['active_items_details']), 3)
        
        # Verify items are sorted by progress (highest first)
        items = details['active_items_details']
        self.assertEqual(items[0]['progress_percentage'], 80)
        self.assertEqual(items[1]['progress_percentage'], 50)
        self.assertEqual(items[2]['progress_percentage'], 20)
        
        # Verify recommendations
        self.assertIn('recommendations', details)
        self.assertEqual(len(details['recommendations']), 3)
        
        # Check that recommendation suggests completing the 80% item
        complete_rec = details['recommendations'][0]
        self.assertEqual(complete_rec['action'], 'complete_closest')
        self.assertEqual(complete_rec['item']['progress_percentage'], 80)
        
        # Check that recommendation suggests pausing the 20% item
        pause_rec = details['recommendations'][1]
        self.assertEqual(pause_rec['action'], 'pause_least_progress')
        self.assertEqual(pause_rec['item']['progress_percentage'], 20)
    
    def test_validate_item_addition_success(self):
        """Test validation passes with valid data and capacity"""
        item_data = {
            'title': 'Python Course',
            'source_type': 'course',
            'source_url': 'https://example.com/course'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, item_data)
        
        self.assertTrue(result['is_valid'])
        self.assertTrue(result['can_proceed'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_item_addition_missing_required_field(self):
        """Test validation fails with missing required field"""
        item_data = {
            'source_type': 'course'
            # Missing 'title'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, item_data)
        
        self.assertFalse(result['is_valid'])
        self.assertFalse(result['can_proceed'])
        self.assertGreater(len(result['errors']), 0)
        self.assertEqual(result['errors'][0]['field'], 'title')
    
    def test_validate_item_addition_invalid_source_type(self):
        """Test validation fails with invalid source type"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'invalid_type'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, item_data)
        
        self.assertFalse(result['is_valid'])
        self.assertFalse(result['can_proceed'])
        error_fields = [e['field'] for e in result['errors']]
        self.assertIn('source_type', error_fields)
    
    def test_validate_item_addition_at_capacity_limit(self):
        """Test validation fails when at capacity limit"""
        # Create 3 active items
        for i in range(3):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Try to validate adding 4th item
        new_item_data = {
            'title': 'Course 4',
            'source_type': 'course'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, new_item_data)
        
        self.assertFalse(result['is_valid'])
        self.assertFalse(result['can_proceed'])
        self.assertGreater(len(result['errors']), 0)
        
        # Check capacity error
        capacity_error = next((e for e in result['errors'] if e['field'] == 'capacity'), None)
        self.assertIsNotNone(capacity_error)
        self.assertIn('details', capacity_error)
    
    def test_validate_item_addition_with_warning(self):
        """Test validation succeeds but includes warning when approaching limit"""
        # Create 2 active items
        for i in range(2):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Validate adding 3rd item
        new_item_data = {
            'title': 'Course 3',
            'source_type': 'course'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, new_item_data)
        
        self.assertTrue(result['is_valid'])
        self.assertTrue(result['can_proceed'])
        self.assertGreater(len(result['warnings']), 0)
        
        # Check for approaching limit warning
        warning = next((w for w in result['warnings'] if w['type'] == 'approaching_limit'), None)
        self.assertIsNotNone(warning)
    
    def test_validate_item_addition_with_force_bypass(self):
        """Test validation with force flag bypasses capacity check"""
        # Create 3 active items
        for i in range(3):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Validate with force=True (admin override)
        new_item_data = {
            'title': 'Course 4',
            'source_type': 'course'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, new_item_data, force=True)
        
        self.assertTrue(result['is_valid'])
        self.assertTrue(result['can_proceed'])
        # Should not have capacity error when forced
        capacity_errors = [e for e in result['errors'] if e.get('field') == 'capacity']
        self.assertEqual(len(capacity_errors), 0)
    
    def test_validate_item_addition_url_warning(self):
        """Test validation includes warning for invalid URL format"""
        item_data = {
            'title': 'Test Course',
            'source_type': 'course',
            'source_url': 'invalid-url-format'
        }
        
        result = InboxService.validate_item_addition(self.test_user.id, item_data)
        
        self.assertTrue(result['is_valid'])  # Still valid, just a warning
        self.assertGreater(len(result['warnings']), 0)
        
        # Check for URL warning
        url_warning = next((w for w in result['warnings'] if w['type'] == 'invalid_url'), None)
        self.assertIsNotNone(url_warning)
    
    def test_blocking_prevents_actual_item_creation(self):
        """Test that create_learning_item actually blocks when at limit"""
        # Create 3 active items
        for i in range(3):
            item_data = {
                'title': f'Course {i+1}',
                'source_type': 'course'
            }
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        # Try to create 4th item - should raise ValueError
        item_data = {
            'title': 'Course 4',
            'source_type': 'course'
        }
        
        with self.assertRaises(ValueError) as context:
            InboxService.create_learning_item(self.test_user.id, item_data)
        
        self.assertIn('Cannot add new item', str(context.exception))
        self.assertIn('3 active items', str(context.exception))
        
        # Verify only 3 items exist
        items = InboxService.get_user_items(self.test_user.id)
        self.assertEqual(len(items), 3)


if __name__ == '__main__':
    unittest.main()
