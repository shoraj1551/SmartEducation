"""
Pod Sharing Service - Handles privacy-controlled content sharing
"""
from app.models import User
from app.pod_models import SharedContent, PodMessage
from datetime import datetime


class PodSharingService:
    
    @staticmethod
    def share_content(user_id, content_type, content_id, content_title, partner_ids, permissions=None):
        """
        Share content with specific partners
        
        Args:
            user_id: Owner's user ID
            content_type: 'course', 'commitment', 'task', 'bookmark'
            content_id: ID of the content
            content_title: Title for display
            partner_ids: List of partner user IDs to share with
            permissions: Dict with share_progress, share_tasks, share_notes
        """
        # Check if already shared
        existing = SharedContent.objects(
            user_id=user_id,
            content_type=content_type,
            content_id=content_id
        ).first()
        
        if existing:
            # Update existing share
            existing.shared_with = [User.objects.get(id=pid) for pid in partner_ids]
            if permissions:
                existing.share_progress = permissions.get('share_progress', True)
                existing.share_tasks = permissions.get('share_tasks', True)
                existing.share_notes = permissions.get('share_notes', False)
            existing.updated_at = datetime.utcnow()
            existing.save()
            return existing.to_dict()
        
        # Create new share
        partners = [User.objects.get(id=pid) for pid in partner_ids]
        
        shared = SharedContent(
            user_id=User.objects.get(id=user_id),
            content_type=content_type,
            content_id=content_id,
            content_title=content_title,
            shared_with=partners,
            share_progress=permissions.get('share_progress', True) if permissions else True,
            share_tasks=permissions.get('share_tasks', True) if permissions else True,
            share_notes=permissions.get('share_notes', False) if permissions else False
        )
        shared.save()
        return shared.to_dict()
    
    @staticmethod
    def unshare_content(user_id, share_id):
        """Remove a share"""
        shared = SharedContent.objects.get(id=share_id, user_id=user_id)
        shared.delete()
        return True
    
    @staticmethod
    def get_my_shared_content(user_id):
        """Get all content I've shared with others"""
        shares = SharedContent.objects(user_id=user_id)
        return [s.to_dict() for s in shares]
    
    @staticmethod
    def get_shared_with_me(user_id):
        """Get all content others have shared with me"""
        user = User.objects.get(id=user_id)
        shares = SharedContent.objects(shared_with=user)
        
        result = []
        for share in shares:
            data = share.to_dict()
            # Add owner info
            data['owner_name'] = share.user_id.name
            data['owner_email'] = share.user_id.email
            result.append(data)
        
        return result
    
    @staticmethod
    def send_message(sender_id, receiver_id, message_text):
        """Send a message to a pod partner"""
        msg = PodMessage(
            sender_id=User.objects.get(id=sender_id),
            receiver_id=User.objects.get(id=receiver_id),
            message=message_text
        )
        msg.save()
        return msg.to_dict()
    
    @staticmethod
    def get_messages(user_id, partner_id, limit=50):
        """Get message thread with a specific partner"""
        user = User.objects.get(id=user_id)
        partner = User.objects.get(id=partner_id)
        
        # Get messages in both directions
        messages = PodMessage.objects(
            (Q(sender_id=user) & Q(receiver_id=partner)) |
            (Q(sender_id=partner) & Q(receiver_id=user))
        ).order_by('-created_at').limit(limit)
        
        # Mark received messages as read
        PodMessage.objects(
            sender_id=partner,
            receiver_id=user,
            is_read=False
        ).update(is_read=True)
        
        return [m.to_dict() for m in reversed(list(messages))]
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread messages"""
        user = User.objects.get(id=user_id)
        return PodMessage.objects(receiver_id=user, is_read=False).count()
