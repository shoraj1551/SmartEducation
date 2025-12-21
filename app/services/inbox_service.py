"""
Inbox Service for Unified Learning Inbox Feature
Handles CRUD operations and business logic for learning items
"""
from datetime import datetime
from app.models import LearningItem, ContentSource, User
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

        # ---------------------------------------------------------
        # Adapter Integration: Auto-Fetch Metadata
        # ---------------------------------------------------------
        from app.services.adapters.factory import AdapterFactory
        
        # If we have a URL but missing details (title/duration), try to fetch them
        if 'source_url' in item_data and item_data['source_url']:
            adapter = AdapterFactory.get_adapter(item_data['source_url'])
            if adapter:
                try:
                    metadata = adapter.fetch_metadata(item_data['source_url'])
                    
                    # Auto-fill missing fields
                    if 'title' not in item_data or not item_data['title']:
                        item_data['title'] = metadata.get('title', 'Untitled Content')
                    
                    if 'description' not in item_data:
                        item_data['description'] = metadata.get('description', '')
                        
                    if 'total_duration' not in item_data or item_data['total_duration'] == 0:
                        item_data['total_duration'] = metadata.get('duration_minutes', 0)
                        
                    # Merge metadata
                    if 'metadata' not in item_data:
                        item_data['metadata'] = {}
                    item_data['metadata'].update(metadata.get('platform_metadata', {}))
                    
                    # Set thumbnail if available (storing in metadata for now)
                    if 'thumbnail_url' in metadata:
                        item_data['metadata']['thumbnail_url'] = metadata['thumbnail_url']
                        
                except Exception as e:
                    # Don't fail the creation, just log/ignore and proceed with defaults
                    print(f"Metadata fetch failed: {e}")

        # Final check for Title (in case adapter failed and user didn't provide one)
        if 'title' not in item_data or not item_data['title']:
             raise ValueError("Title is required (could not be auto-fetched)")
        
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
    
    @staticmethod
    def check_can_add_item(user_id):
        """
        Check if user can add a new item and provide detailed feedback
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with can_add boolean and detailed message
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return {
                'can_add': False,
                'reason': 'User not found',
                'active_items': [],
                'suggestions': []
            }
        
        active_items = LearningItem.objects(user_id=user, status='active')
        active_count = active_items.count()
        
        can_add = active_count < InboxService.MAX_ACTIVE_ITEMS
        
        result = {
            'can_add': can_add,
            'active_count': active_count,
            'max_allowed': InboxService.MAX_ACTIVE_ITEMS,
            'slots_available': max(0, InboxService.MAX_ACTIVE_ITEMS - active_count)
        }
        
        if not can_add:
            # Provide detailed blocking information
            result['reason'] = f'Maximum active items limit reached ({active_count}/{InboxService.MAX_ACTIVE_ITEMS})'
            result['active_items'] = [
                {
                    'id': str(item.id),
                    'title': item.title,
                    'progress_percentage': item.progress_percentage,
                    'added_at': item.added_at.isoformat() if item.added_at else None
                }
                for item in active_items
            ]
            result['suggestions'] = [
                'Complete an existing learning item to free up a slot',
                'Pause a learning item you\'re not currently working on',
                'Drop a learning item you no longer wish to pursue'
            ]
            result['message'] = (
                f"You have reached the maximum limit of {InboxService.MAX_ACTIVE_ITEMS} active learning items. "
                f"To maintain focus and prevent content hoarding, please complete, pause, or drop "
                f"one of your existing items before adding new content."
            )
        else:
            # Provide warning if approaching limit
            if active_count == InboxService.MAX_ACTIVE_ITEMS - 1:
                result['warning'] = f'You have {active_count} active items. Only 1 slot remaining!'
                result['message'] = 'You can add this item, but you\'re at your limit. Focus on completing current items.'
            else:
                result['message'] = f'You can add new items. {result["slots_available"]} slots available.'
        
        return result
    
    @staticmethod
    def get_blocking_details(user_id):
        """
        Get detailed information about why adding new items is blocked
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with blocking details and recommendations
        """
        check_result = InboxService.check_can_add_item(user_id)
        
        if check_result['can_add']:
            return {
                'is_blocked': False,
                'message': 'You can add new learning items'
            }
        
        # Calculate additional metrics for blocked users
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return {'is_blocked': True, 'message': 'User not found'}
        
        active_items = LearningItem.objects(user_id=user, status='active')
        
        # Find items closest to completion
        items_with_progress = []
        for item in active_items:
            items_with_progress.append({
                'id': str(item.id),
                'title': item.title,
                'progress_percentage': item.progress_percentage,
                'remaining_percentage': 100 - item.progress_percentage,
                'total_duration': item.total_duration,
                'completed_duration': item.completed_duration,
                'remaining_duration': item.total_duration - item.completed_duration
            })
        
        # Sort by progress (highest first)
        items_with_progress.sort(key=lambda x: x['progress_percentage'], reverse=True)
        
        return {
            'is_blocked': True,
            'reason': check_result['reason'],
            'active_count': check_result['active_count'],
            'max_allowed': check_result['max_allowed'],
            'message': check_result['message'],
            'active_items_details': items_with_progress,
            'recommendations': [
                {
                    'action': 'complete_closest',
                    'description': 'Focus on completing the item closest to 100%',
                    'item': items_with_progress[0] if items_with_progress else None
                },
                {
                    'action': 'pause_least_progress',
                    'description': 'Pause the item with least progress if you\'re not actively working on it',
                    'item': items_with_progress[-1] if items_with_progress else None
                },
                {
                    'action': 'review_all',
                    'description': 'Review all active items and decide which to keep, pause, or drop'
                }
            ]
        }
    
    @staticmethod
    def validate_item_addition(user_id, item_data, force=False):
        """
        Comprehensive validation before adding a new item
        
        Args:
            user_id: User ID
            item_data: Item data to validate
            force: If True, bypass capacity checks (admin override)
            
        Returns:
            Dictionary with validation result
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'can_proceed': True
        }
        
        # Check capacity unless forced
        if not force:
            capacity_check = InboxService.check_can_add_item(user_id)
            if not capacity_check['can_add']:
                validation_result['is_valid'] = False
                validation_result['can_proceed'] = False
                validation_result['errors'].append({
                    'field': 'capacity',
                    'message': capacity_check['message'],
                    'details': capacity_check
                })
                return validation_result
            
            # Add warning if approaching limit
            if 'warning' in capacity_check:
                validation_result['warnings'].append({
                    'type': 'approaching_limit',
                    'message': capacity_check['warning']
                })
        
        # Validate required fields
        required_fields = ['title', 'source_type']
        for field in required_fields:
            if field not in item_data or not item_data[field]:
                validation_result['is_valid'] = False
                validation_result['errors'].append({
                    'field': field,
                    'message': f'Missing required field: {field}'
                })
        
        # Validate source_type
        valid_source_types = ['course', 'video', 'pdf', 'bookmark', 'playlist', 'article']
        if 'source_type' in item_data and item_data['source_type'] not in valid_source_types:
            validation_result['is_valid'] = False
            validation_result['errors'].append({
                'field': 'source_type',
                'message': f'Invalid source_type. Must be one of: {", ".join(valid_source_types)}'
            })
        
        # Validate URL format if provided
        if 'source_url' in item_data and item_data['source_url']:
            url = item_data['source_url']
            if not (url.startswith('http://') or url.startswith('https://')):
                validation_result['warnings'].append({
                    'type': 'invalid_url',
                    'message': 'Source URL should start with http:// or https://'
                })
        
        validation_result['can_proceed'] = validation_result['is_valid']
        return validation_result

    @staticmethod
    def import_from_bookmark(user_id, bookmark_id):
        """
        Promote a Library Bookmark to an Active Inbox Item
        
        Args:
            user_id: User ID
            bookmark_id: Bookmark ID
            
        Returns:
            Created LearningItem
        """
        from app.models import Bookmark
        
        # 1. Verify User and Bookmark
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
                
            bookmark = Bookmark.objects.get(id=bookmark_id, user=user)
        except DoesNotExist:
            raise ValueError("Bookmark not found or access denied")

        # 2. Check Capacity (Strict Mode)
        capacity = InboxService.check_can_add_item(user)
        if not capacity['can_add']:
             raise ValueError(capacity['message'])

        # 3. Check if already imported (prevent duplicates)
        # We check if an active item has the same source URL
        existing = LearningItem.objects(
            user_id=user, 
            source_url=bookmark.url, 
            status__ne='dropped'
        ).first()
        
        if existing:
             raise ValueError(f"This item is already in your inbox as '{existing.title}' ({existing.status})")

        # 4. Create Learning Item
        item = LearningItem(
            user_id=user,
            title=bookmark.title,
            description=bookmark.description,
            source_type=bookmark.resource_type or 'bookmark',
            source_url=bookmark.url,
            platform=bookmark.source,
            status='active',
            priority_score=bookmark.relevance_score,
            tags=bookmark.tags,
            category=bookmark.category,
            metadata=bookmark.meta_data or {}
        )
        item.save()
        
        # 5. Update Bookmark Status
        bookmark.status = 'in_progress'
        bookmark.save()
        
        return item

