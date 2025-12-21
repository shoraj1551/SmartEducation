
"""
Trigger Service (Feature 11)
Context-Aware Logic for Proactive Nudges.
"""
from app.models import User, Notification, DailyTask, Commitment
from datetime import datetime, timedelta

class TriggerService:
    
    @staticmethod
    def evaluate_context(user_id):
        """
        Analyze user context and trigger notifications.
        Should be called periodically or on dashboard load.
        """
        check_log = []
        user = User.objects.get(id=user_id)
        now = datetime.utcnow()
        # Adjust for TZ? Assuming UTC or keeping simple for MVP (System time).
        # In a real app, user.timezone is critical.
        
        # 1. Evening Nudge (Warning)
        # If after 8PM (20:00) and no tasks completed
        if now.hour >= 20: 
            completed_today = DailyTask.objects(
                user_id=user_id,
                status='completed',
                completed_at__gte=now.replace(hour=0, minute=0)
            ).count()
            
            if completed_today == 0:
                TriggerService.create_notification(
                    user_id,
                    "Streak Risk ⚠️",
                    "The day is almost over. Complete 1 small task to keep your momentum.",
                    "warning"
                )
                check_log.append("Evening Nudge Triggered")

        # 2. Morning Planner (Info)
        # If Morning (6am-10am) and no tasks for today
        if 6 <= now.hour <= 10:
            tasks_today = DailyTask.objects(
                user_id=user_id,
                scheduled_date__gte=now.replace(hour=0, minute=0),
                scheduled_date__lt=now.replace(hour=23, minute=59)
            ).count()
            
            if tasks_today == 0:
                TriggerService.create_notification(
                    user_id,
                    "Plan Your Victory 🌅",
                    "No tasks scheduled for today yet. Define your goals now.",
                    "info",
                    link="/schedule"
                )
                check_log.append("Morning Plan Triggered")
        
        # 3. Burnout Warning (Health)
        # If Burnout Level is High (Check BurnoutService logic or replicate simple check)
        # Simple check: > 10 tasks pending?
        pending_count = DailyTask.objects(user_id=user_id, status='pending').count()
        if pending_count > 15:
             TriggerService.create_notification(
                user_id,
                "Overload Detected 🛑",
                f"You have {pending_count} pending tasks. Prioritize or Reschedule.",
                "error",
                link="/schedule"
            )

        return check_log

    @staticmethod
    def create_notification(user_id, title, message, type='info', link=None):
        """
        Create notification if not already sent recently (Anti-Spam).
        """
        # Anti-spam: Check if same title sent in last 12 hours
        cutoff = datetime.utcnow() - timedelta(hours=12)
        exists = Notification.objects(
            user_id=user_id,
            title=title,
            created_at__gte=cutoff
        ).first()
        
        if not exists:
            n = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=type,
                action_link=link
            )
            n.save()
            return True
        return False

    @staticmethod
    def get_notifications(user_id, unread_only=True):
        qs = Notification.objects(user_id=user_id)
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs.order_by('-created_at')

    @staticmethod
    def mark_read(notif_id):
        n = Notification.objects.get(id=notif_id)
        n.is_read = True
        n.save()
