"""
Video Guard Service for Feature 7: Anti-Distraction Video Learning Guard
Handles video access control and distraction prevention
"""
from datetime import datetime
from app.models import LearningItem, User
from mongoengine.errors import DoesNotExist


class VideoGuardService:
    """Service for managing video access control and distraction prevention"""
    
    @staticmethod
    def create_video_whitelist(learning_item_id, video_urls):
        """
        Create whitelist of allowed videos for a learning item
        
        Args:
            learning_item_id: Learning item ID
            video_urls: List of allowed video URLs
            
        Returns:
            Updated learning item
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        # Store whitelist in metadata
        if not item.metadata:
            item.metadata = {}
        
        item.metadata['video_whitelist'] = video_urls
        item.metadata['whitelist_created_at'] = datetime.utcnow().isoformat()
        item.save()
        
        return item
    
    @staticmethod
    def is_video_allowed(learning_item_id, video_url):
        """
        Check if a video URL is in the whitelist
        
        Args:
            learning_item_id: Learning item ID
            video_url: Video URL to check
            
        Returns:
            Boolean indicating if video is allowed
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            return False
        
        if not item.metadata or 'video_whitelist' not in item.metadata:
            return True  # No whitelist = all allowed
        
        whitelist = item.metadata['video_whitelist']
        
        # Check if URL is in whitelist (exact match or contains)
        for allowed_url in whitelist:
            if allowed_url in video_url or video_url in allowed_url:
                return True
        
        return False
    
    @staticmethod
    def track_video_watch(learning_item_id, video_url, watch_data):
        """
        Track video watch progress
        
        Args:
            learning_item_id: Learning item ID
            video_url: Video URL being watched
            watch_data: Dictionary with watch details (duration, progress, etc.)
            
        Returns:
            Updated learning item
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        if not item.metadata:
            item.metadata = {}
        
        if 'video_watch_history' not in item.metadata:
            item.metadata['video_watch_history'] = []
        
        # Add watch record
        watch_record = {
            'video_url': video_url,
            'timestamp': datetime.utcnow().isoformat(),
            'duration_watched': watch_data.get('duration_watched', 0),
            'total_duration': watch_data.get('total_duration', 0),
            'progress_percentage': watch_data.get('progress_percentage', 0),
            'completed': watch_data.get('completed', False)
        }
        
        item.metadata['video_watch_history'].append(watch_record)
        item.save()
        
        return item
    
    @staticmethod
    def log_distraction_attempt(learning_item_id, distraction_type, details=None):
        """
        Log a distraction attempt during video learning
        
        Args:
            learning_item_id: Learning item ID
            distraction_type: Type of distraction (navigation, new_tab, etc.)
            details: Additional details
            
        Returns:
            Updated learning item
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        if not item.metadata:
            item.metadata = {}
        
        if 'distraction_log' not in item.metadata:
            item.metadata['distraction_log'] = []
        
        # Add distraction record
        distraction_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': distraction_type,
            'details': details or {}
        }
        
        item.metadata['distraction_log'].append(distraction_record)
        item.save()
        
        return item
    
    @staticmethod
    def get_video_stats(learning_item_id):
        """
        Get video watching statistics for a learning item
        
        Args:
            learning_item_id: Learning item ID
            
        Returns:
            Dictionary with video statistics
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        if not item.metadata:
            return {
                'total_videos_watched': 0,
                'total_watch_time': 0,
                'completed_videos': 0,
                'distraction_attempts': 0
            }
        
        watch_history = item.metadata.get('video_watch_history', [])
        distraction_log = item.metadata.get('distraction_log', [])
        
        # Calculate stats
        total_videos = len(set(record['video_url'] for record in watch_history))
        total_watch_time = sum(record.get('duration_watched', 0) for record in watch_history)
        completed_videos = sum(1 for record in watch_history if record.get('completed', False))
        distraction_attempts = len(distraction_log)
        
        return {
            'total_videos_watched': total_videos,
            'total_watch_time_minutes': round(total_watch_time / 60, 2),
            'completed_videos': completed_videos,
            'distraction_attempts': distraction_attempts,
            'focus_score': VideoGuardService._calculate_focus_score(total_watch_time, distraction_attempts)
        }
    
    @staticmethod
    def _calculate_focus_score(watch_time_seconds, distraction_count):
        """
        Calculate focus score (0-100)
        Higher = better focus
        """
        if watch_time_seconds == 0:
            return 0
        
        # Convert to minutes
        watch_time_minutes = watch_time_seconds / 60
        
        # Calculate distractions per hour
        distractions_per_hour = (distraction_count / watch_time_minutes) * 60 if watch_time_minutes > 0 else 0
        
        # Score: 100 - (distractions per hour * 10)
        # 0 distractions = 100, 10 distractions/hour = 0
        score = max(0, 100 - (distractions_per_hour * 10))
        
        return round(score, 2)
    
    @staticmethod
    def get_allowed_videos(learning_item_id):
        """Get list of allowed videos for a learning item"""
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        if not item.metadata or 'video_whitelist' not in item.metadata:
            return []
        
        return item.metadata['video_whitelist']
