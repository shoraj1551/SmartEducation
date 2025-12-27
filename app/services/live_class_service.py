"""
Live Class Service
Handles live online class sessions (Google Meet, Zoom, etc.)
"""
from datetime import datetime
from app.models import LiveClass, User
from mongoengine.errors import DoesNotExist


class LiveClassService:
    """Service layer for managing live class sessions"""
    
    @staticmethod
    def create_class(user_id, meeting_url, title=None, platform='custom', **kwargs):
        """
        Create a new live class session
        
        Args:
            user_id: User ID
            meeting_url: Meeting URL (required)
            title: Optional title for the class
            platform: Platform type (google_meet, zoom, custom)
            **kwargs: Additional optional fields (description, scheduled_at, etc.)
            
        Returns:
            Created LiveClass object
        """
        # Get user
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Create live class
        live_class = LiveClass(
            user_id=user,
            meeting_url=meeting_url,
            title=title or f"{platform.replace('_', ' ').title()} Class",
            platform=platform,
            description=kwargs.get('description', ''),
            meeting_id=kwargs.get('meeting_id', ''),
            passcode=kwargs.get('passcode', ''),
            scheduled_at=kwargs.get('scheduled_at'),
            duration_minutes=kwargs.get('duration_minutes', 60),
            tags=kwargs.get('tags', []),
            category=kwargs.get('category', '')
        )
        
        live_class.save()
        return live_class
    
    @staticmethod
    def join_class(class_id, user_id):
        """
        Mark a class as joined and update timestamp
        
        Args:
            class_id: LiveClass ID
            user_id: User ID
            
        Returns:
            Updated LiveClass object with meeting URL
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
                
            live_class = LiveClass.objects.get(id=class_id, user_id=user)
        except DoesNotExist:
            raise ValueError("Live class not found or access denied")
        
        # Update joined timestamp
        if not live_class.joined_at:
            live_class.joined_at = datetime.utcnow()
            live_class.save()
        
        return live_class
    
    @staticmethod
    def end_class(class_id, user_id):
        """
        Mark a class as ended
        
        Args:
            class_id: LiveClass ID
            user_id: User ID
            
        Returns:
            Updated LiveClass object
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
                
            live_class = LiveClass.objects.get(id=class_id, user_id=user)
        except DoesNotExist:
            raise ValueError("Live class not found or access denied")
        
        # Update ended timestamp
        if not live_class.ended_at:
            live_class.ended_at = datetime.utcnow()
            live_class.save()
        
        return live_class
    
    @staticmethod
    def get_user_classes(user_id, limit=None, skip=0):
        """
        Get all live classes for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of classes to return
            skip: Number of classes to skip (for pagination)
            
        Returns:
            List of LiveClass objects
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        query = LiveClass.objects(user_id=user)
        
        # Sort by created date (newest first)
        query = query.order_by('-created_at')
        
        if skip:
            query = query.skip(skip)
        
        if limit:
            query = query.limit(limit)
        
        return list(query)
    
    @staticmethod
    def get_upcoming_classes(user_id):
        """
        Get upcoming scheduled classes
        
        Args:
            user_id: User ID
            
        Returns:
            List of LiveClass objects scheduled in the future
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        now = datetime.utcnow()
        
        classes = LiveClass.objects(
            user_id=user,
            scheduled_at__gte=now
        ).order_by('scheduled_at')
        
        return list(classes)
    
    @staticmethod
    def get_past_classes(user_id, limit=10):
        """
        Get past classes (joined or ended)
        
        Args:
            user_id: User ID
            limit: Maximum number of classes to return
            
        Returns:
            List of LiveClass objects
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        classes = LiveClass.objects(
            user_id=user,
            joined_at__exists=True
        ).order_by('-joined_at').limit(limit)
        
        return list(classes)
