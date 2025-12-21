
"""
Accountability Service (Feature 13)
Social Logic: Invites, Pods, Nudges.
"""
from app.models import User, AccountabilityPartner, DailyTask, Notification, Commitment
from datetime import datetime

class AccountabilityService:
    
    @staticmethod
    def send_invite(user_id, partner_email):
        # Prevent self-invite
        sender = User.objects.get(id=user_id)
        if sender.email == partner_email:
            raise ValueError("Cannot invite yourself.")
            
        # Check if already invited
        existing = AccountabilityPartner.objects(
            user_id=user_id, 
            partner_email=partner_email
        ).first()
        
        if existing:
            if existing.status == 'active': return "Already partners."
            return "Invite already sent."
            
        # Create Invite
        # Check if partner exists as user
        partner_user = User.objects(email=partner_email).first()
        
        AccountabilityPartner(
            user_id=user_id,
            partner_email=partner_email,
            partner_user_id=partner_user if partner_user else None,
            status='pending'
        ).save()
        
        # If user exists, create notification for them
        if partner_user:
            Notification(
                user_id=partner_user.id,
                title="Pod Invite 🤝",
                message=f"{sender.name} invited you to join their Accountability Pod.",
                notification_type="info",
                action_link="/pods"
            ).save()
            
        return "Invite sent."

    @staticmethod
    def accept_invite(invite_id, user_id):
        # We need to find the invite where partner_email matches current user's email
        # BUT invite_id provided refers to the specific record created by sender?
        # Actually, let's look up by ID.
        invite = AccountabilityPartner.objects.get(id=invite_id)
        accepter = User.objects.get(id=user_id)
        
        if invite.partner_email != accepter.email:
            raise ValueError("Email mismatch.")
            
        invite.status = 'active'
        invite.partner_user_id = accepter
        invite.accepted_at = datetime.utcnow()
        invite.save()
        
        # Create Reverse Link immediately so connection is bidirectional
        # Check if reverse exists
        reverse = AccountabilityPartner.objects(
            user_id=accepter.id,
            partner_email=invite.user_id.email
        ).first()
        
        if not reverse:
            AccountabilityPartner(
                user_id=accepter.id,
                partner_email=invite.user_id.email,
                partner_user_id=invite.user_id,
                status='active',
                accepted_at=datetime.utcnow()
            ).save()
        else:
            reverse.status = 'active'
            reverse.partner_user_id = invite.user_id
            reverse.save()
            
        return "Pod joined."

    @staticmethod
    def get_pod(user_id):
        # Get active partners
        partners = AccountabilityPartner.objects(
            user_id=user_id,
            status='active'
        )
        
        pod_data = []
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0)
        
        for p in partners:
            if not p.partner_user_id: continue
            
            u = p.partner_user_id
            # Calculate stats
            tasks_today = DailyTask.objects(
                user_id=u.id, 
                status='completed',
                completed_at__gte=today_start
            ).count()
            
            # Simple streak lookup (assuming we store it on User or calculate)
            # User model doesn't explicitly have streak field in previous version? 
            # Checked models.py: User has `xp_total`, `level`. Commitment has `current_streak`.
            # We'll sum active commitment streaks or use a generic one if implemented. 
            # For MVP, let's use DailyTask data to estimate or just show XP Level.
            streak = 0 # Placeholder
            
            pod_data.append({
                'id': str(u.id),
                'name': u.name,
                'email': u.email,
                'level': u.level,
                'xp': u.xp_total,
                'tasks_today': tasks_today,
                'status': 'online' # Placeholder
            })
            
        return pod_data

    @staticmethod
    def nudge_partner(sender_id, partner_id):
        sender = User.objects.get(id=sender_id)
        partner = User.objects.get(id=partner_id)
        
        Notification(
            user_id=partner.id,
            title="Nudge from Pod 👋",
            message=f"{sender.name} says: Time to focus!",
            notification_type="warning"
        ).save()
        return True
