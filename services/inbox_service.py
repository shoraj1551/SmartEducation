"""
Inbox Service for Unified Learning Inbox Feature
Handles CRUD operations and business logic for learning items
"""
from datetime import datetime
from models import LearningItem, ContentSource, User
from mongoengine.errors import ValidationError, DoesNotExist


class InboxService:
    """Service layer for managing learning items in the unified inbox"""
    
    # Configuration
    MAX_ACTIVE_ITEMS = 3  # Maximum number of active learning items per user
    
    @staticmethod
    def create_learning_item(user_id, item_data):
        """
        Create a new learning item with validation
        
        Args:
            user_id: User ID (string or User object)
            item_data: Dictionary containing item details
            
        Returns:
            Created LearningItem object
            
        Raises:
            ValueError: If validation fails
        """
        # Get user object
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Check if user has reached max active items limit
        active_count = LearningItem.objects(
            user_id=user,
            status='active'
        ).count()
        
        if active_count >= InboxService.MAX_ACTIVE_ITEMS:
            raise ValueError(
                f"Cannot add new item. You have {active_count} active items. "
                f"Please complete or pause existing items before adding new ones. "
                f"(Maximum: {InboxService.MAX_ACTIVE_ITEMS} active items)"
            )
        
        # Validate required fields
        required_fields = ['title', 'source_type']
        for field in required_fields:
            if field not in item_data or not item_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate source_type
        valid_source_types = ['course', 'video', 'pdf', 'bookmark', 'playlist', 'article']
        if item_data['source_type'] not in valid_source_types:
            raise ValueError(f"Invalid source_type. Must be one of: {', '.join(valid_source_types)}")
        
        # Create the learning item
        learning_item = LearningItem(
            user_id=user,
            title=item_data['title'],
            description=item_data.get('description', ''),
            source_type=item_data['source_type'],
            source_url=item_data.get('source_url', ''),
            platform=item_data.get('platform', ''),
            status='active',  # New items start as active
            total_duration=item_data.get('total_duration', 0),
            metadata=item_data.get('metadata', {}),
            target_completion_date=item_data.get('target_completion_date'),
            tags=item_data.get('tags', []),
            category=item_data.get('category', '')
        )
        
        learning_item.save()
        return learning_item
    
    @staticmethod
    def get_user_items(user_id, status_filter=None, limit=None, skip=0):
        """
        Get learning items for a user with optional filtering
        
        Args:
            user_id: User ID
            status_filter: Optional status to filter by (active, paused, completed, dropped)
            limit: Maximum number of items to return
            skip: Number of items to skip (for pagination)
            
        Returns:
            List of LearningItem objects
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        query = LearningItem.objects(user_id=user)
        
        if status_filter:
            query = query.filter(status=status_filter)
        
        # Sort by priority score (descending) and added date (newest first)
        query = query.order_by('-priority_score', '-added_at')
        
        if skip:
            query = query.skip(skip)
        
        if limit:
            query = query.limit(limit)
        
        return list(query)
    
    @staticmethod
    def get_item_by_id(item_id, user_id=None):
        """
        Get a specific learning item by ID
        
        Args:
            item_id: Learning item ID
            user_id: Optional user ID for ownership verification
            
        Returns:
            LearningItem object or None
        """
        try:
            item = LearningItem.objects.get(id=item_id)
            
            # Verify ownership if user_id provided
            if user_id and str(item.user_id.id) != str(user_id):
                return None
            
            return item
        except DoesNotExist:
            return None
    
    @staticmethod
    def update_item_status(item_id, new_status, user_id=None):
        """
        Update the status of a learning item with validation
        
        Args:
            item_id: Learning item ID
            new_status: New status (active, paused, completed, dropped)
            user_id: Optional user ID for ownership verification
            
        Returns:
            Updated LearningItem object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate status
        valid_statuses = ['active', 'paused', 'completed', 'dropped']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        # Get item
        item = InboxService.get_item_by_id(item_id, user_id)
        if not item:
            raise ValueError("Learning item not found or access denied")
        
        # Check active items limit when changing to active
        if new_status == 'active' and item.status != 'active':
            active_count = LearningItem.objects(
                user_id=item.user_id,
                status='active'
            ).count()
            
            if active_count >= InboxService.MAX_ACTIVE_ITEMS:
                raise ValueError(
                    f"Cannot activate item. You already have {active_count} active items. "
                    f"Please pause or complete an existing item first."
                )
        
        # Update status and timestamps
        old_status = item.status
        item.status = new_status
        
        if new_status == 'paused':
            item.paused_at = datetime.utcnow()
        elif new_status == 'completed':
            item.completed_at = datetime.utcnow()
            item.progress_percentage = 100.0
        elif new_status == 'active' and old_status != 'active':
            if not item.started_at:
                item.started_at = datetime.utcnow()
        
        item.save()
        return item
    
    @staticmethod
    def update_progress(item_id, completed_duration, user_id=None):
        """
        Update the progress of a learning item
        
        Args:
            item_id: Learning item ID
            completed_duration: Completed duration in minutes
            user_id: Optional user ID for ownership verification
            
        Returns:
            Updated LearningItem object
        """
        item = InboxService.get_item_by_id(item_id, user_id)
        if not item:
            raise ValueError("Learning item not found or access denied")
        
        item.completed_duration = completed_duration
        item.last_accessed_at = datetime.utcnow()
        item.update_progress()
        
        # Auto-complete if progress reaches 100%
        if item.progress_percentage >= 100 and item.status != 'completed':
            item.status = 'completed'
            item.completed_at = datetime.utcnow()
            item.save()
        
        return item
    
    @staticmethod
    def delete_item(item_id, user_id=None):
        """
        Delete a learning item
        
        Args:
            item_id: Learning item ID
            user_id: Optional user ID for ownership verification
            
        Returns:
            True if deleted successfully
        """
        item = InboxService.get_item_by_id(item_id, user_id)
        if not item:
            raise ValueError("Learning item not found or access denied")
        
        item.delete()
        return True
    
    @staticmethod
    def get_inbox_stats(user_id):
        """
        Get statistics about user's learning inbox
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with inbox statistics
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return {}
        
        total_items = LearningItem.objects(user_id=user).count()
        active_items = LearningItem.objects(user_id=user, status='active').count()
        paused_items = LearningItem.objects(user_id=user, status='paused').count()
        completed_items = LearningItem.objects(user_id=user, status='completed').count()
        dropped_items = LearningItem.objects(user_id=user, status='dropped').count()
        
        # Calculate total time invested
        all_items = LearningItem.objects(user_id=user)
        total_time_invested = sum(item.completed_duration for item in all_items)
        
        # Check if user can add new items
        can_add_new = active_items < InboxService.MAX_ACTIVE_ITEMS
        
        return {
            'total_items': total_items,
            'active_items': active_items,
            'paused_items': paused_items,
            'completed_items': completed_items,
            'dropped_items': dropped_items,
            'total_time_invested_minutes': total_time_invested,
            'can_add_new_item': can_add_new,
            'max_active_items': InboxService.MAX_ACTIVE_ITEMS,
            'slots_available': max(0, InboxService.MAX_ACTIVE_ITEMS - active_items)
        }
    
    @staticmethod
    def bulk_update_status(item_ids, new_status, user_id):
        """
        Update status for multiple items at once
        
        Args:
            item_ids: List of item IDs
            new_status: New status to apply
            user_id: User ID for ownership verification
            
        Returns:
            List of updated items
        """
        updated_items = []
        errors = []
        
        for item_id in item_ids:
            try:
                item = InboxService.update_item_status(item_id, new_status, user_id)
                updated_items.append(item)
            except Exception as e:
                errors.append({'item_id': item_id, 'error': str(e)})
        
        return {
            'updated_items': updated_items,
            'errors': errors
        }
