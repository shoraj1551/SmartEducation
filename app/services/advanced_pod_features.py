"""
Advanced Pod Sharing Features - Group Sharing & Activity Feed
"""
from app.models import User
from app.pod_models import SharedContent, PodMessage
from app.services.pod_sharing_service import PodSharingService
from datetime import datetime, timedelta


class AdvancedPodFeatures:
    
    @staticmethod
    def share_with_group(user_id, content_type, content_id, content_title, group_name=None):
        """
        Share content with all pod partners at once (group sharing)
        
        Args:
            user_id: Owner's user ID
            content_type: Type of content
            content_id: Content ID
            content_title: Title
            group_name: Optional group name for organization
        """
        # Get all active pod partners
        from app.services.accountability_service import AccountabilityService
        partners = AccountabilityService.get_pod(user_id)
        
        if not partners:
            return {'error': 'No pod partners found'}
        
        partner_ids = [p['id'] for p in partners]
        
        # Share with all partners
        result = PodSharingService.share_content(
            user_id=user_id,
            content_type=content_type,
            content_id=content_id,
            content_title=content_title,
            partner_ids=partner_ids
        )
        
        # Send notification to all partners
        from app.models import Notification
        user = User.objects.get(id=user_id)
        
        for partner_id in partner_ids:
            Notification(
                user_id=User.objects.get(id=partner_id),
                title="📚 New Shared Content",
                message=f"{user.name} shared '{content_title}' with the pod!",
                notification_type="info",
                action_link="/pods"
            ).save()
        
        return {
            'success': True,
            'shared_with_count': len(partner_ids),
            'partners': [p['name'] for p in partners]
        }
    
    @staticmethod
    def get_activity_feed(user_id, limit=20):
        """
        Get recent activity from pod partners
        
        Returns:
            List of activity items (shares, messages, achievements)
        """
        from app.models import Notification, UserAchievement
        from app.services.accountability_service import AccountabilityService
        
        # Get pod partners
        partners = AccountabilityService.get_pod(user_id)
        partner_ids = [p['id'] for p in partners]
        
        if not partner_ids:
            return []
        
        activities = []
        
        # Recent shares
        recent_shares = SharedContent.objects(
            user_id__in=[User.objects.get(id=pid) for pid in partner_ids]
        ).order_by('-created_at').limit(limit)
        
        for share in recent_shares:
            activities.append({
                'type': 'share',
                'user_name': share.user_id.name,
                'user_id': str(share.user_id.id),
                'content_title': share.content_title,
                'content_type': share.content_type,
                'timestamp': share.created_at.isoformat(),
                'message': f"{share.user_id.name} shared {share.content_title}"
            })
        
        # Recent messages
        recent_messages = PodMessage.objects(
            sender_id__in=[User.objects.get(id=pid) for pid in partner_ids],
            receiver_id=User.objects.get(id=user_id)
        ).order_by('-created_at').limit(10)
        
        for msg in recent_messages:
            activities.append({
                'type': 'message',
                'user_name': msg.sender_id.name,
                'user_id': str(msg.sender_id.id),
                'message': msg.message[:50] + '...' if len(msg.message) > 50 else msg.message,
                'timestamp': msg.created_at.isoformat()
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return activities[:limit]
    
    @staticmethod
    def create_shared_goal(user_id, goal_title, goal_description, target_date, partner_ids):
        """
        Create a shared goal with pod partners
        
        Args:
            user_id: Creator's user ID
            goal_title: Goal title
            goal_description: Description
            target_date: Target completion date
            partner_ids: List of partner IDs to include
        """
        from app.models import Commitment
        
        # Create commitment for creator
        creator_commitment = Commitment(
            user_id=User.objects.get(id=user_id),
            title=goal_title,
            description=goal_description,
            target_date=target_date,
            is_shared_goal=True,
            shared_with=[User.objects.get(id=pid) for pid in partner_ids]
        )
        creator_commitment.save()
        
        # Create linked commitments for partners
        for partner_id in partner_ids:
            partner_commitment = Commitment(
                user_id=User.objects.get(id=partner_id),
                title=goal_title,
                description=goal_description,
                target_date=target_date,
                is_shared_goal=True,
                linked_goal_id=creator_commitment.id
            )
            partner_commitment.save()
            
            # Send notification
            from app.models import Notification
            Notification(
                user_id=User.objects.get(id=partner_id),
                title="🎯 New Shared Goal",
                message=f"You've been added to a shared goal: {goal_title}",
                notification_type="info",
                action_link="/commitments"
            ).save()
        
        return {
            'success': True,
            'goal_id': str(creator_commitment.id),
            'participants': len(partner_ids) + 1
        }
    
    @staticmethod
    def get_pod_leaderboard(user_id):
        """
        Get leaderboard of pod partners based on XP
        """
        from app.services.accountability_service import AccountabilityService
        
        partners = AccountabilityService.get_pod(user_id)
        
        # Add current user
        user = User.objects.get(id=user_id)
        partners.append({
            'id': str(user.id),
            'name': user.name + ' (You)',
            'level': user.level,
            'xp': user.xp_total,
            'tasks_today': 0  # Would calculate from DailyTask
        })
        
        # Sort by XP
        leaderboard = sorted(partners, key=lambda x: x['xp'], reverse=True)
        
        # Add rank
        for i, partner in enumerate(leaderboard):
            partner['rank'] = i + 1
        
        return leaderboard
