
# ============================================================================
# PRIVACY-CONTROLLED POD SHARING
# ============================================================================

from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField, ListField

class SharedContent(Document):
    """Tracks content shared between accountability partners"""
    meta = {'collection': 'shared_content'}
    
    # Owner of the content
    user_id = ReferenceField('User', required=True)
    
    # What is being shared
    content_type = StringField(max_length=50, required=True)  # 'course', 'commitment', 'task', 'bookmark'
    content_id = StringField(required=True)  # ID of the shared item
    content_title = StringField(max_length=300)  # Cached title for quick display
    
    # Who can see it
    shared_with = ListField(ReferenceField('User'))  # List of partner user IDs
    
    # Sharing permissions
    share_progress = BooleanField(default=True)  # Share completion percentage
    share_tasks = BooleanField(default=True)     # Share task completion details
    share_notes = BooleanField(default=False)    # Share personal notes
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'content_type': self.content_type,
            'content_id': self.content_id,
            'content_title': self.content_title,
            'shared_with': [str(u.id) for u in self.shared_with] if self.shared_with else [],
            'share_progress': self.share_progress,
            'share_tasks': self.share_tasks,
            'share_notes': self.share_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PodMessage(Document):
    """Messages between accountability partners"""
    meta = {'collection': 'pod_messages'}
    
    sender_id = ReferenceField('User', required=True)
    receiver_id = ReferenceField('User', required=True)
    message = StringField(required=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'sender_id': str(self.sender_id.id),
            'receiver_id': str(self.receiver_id.id),
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
