from datetime import datetime, time
from app.models import User

class OrchestratorService:
    """
    Central authority for Preference-Aware Learning Orchestration.
    Determines WHEN to contact a user and HOW (tone/content).
    """

    # Time Windows (Local Time - Simplified for MVP, assumes server time or offset)
    # In a real app, strict timezone handling per user is required.
    WINDOWS = {
        'morning': {'start': 5, 'end': 11},      # 5 AM - 11 AM
        'deep_focus': {'start': 9, 'end': 17},   # 9 AM - 5 PM (Work/Focus block)
        'night': {'start': 19, 'end': 1},        # 7 PM - 1 AM
    }

    AI_CONFIGS = {
        'morning': {
            'tone': 'energetic',
            'priority': ['quick_tasks', 'planning', 'concept_review'],
            'motivation': 'Start your day strong!'
        },
        'deep_focus': {
            'tone': 'minimalist',
            'priority': ['long_form', 'deep_work', 'complex_problems'],
            'motivation': 'Stay focused. Deep work in progress.'
        },
        'night': {
            'tone': 'calm',
            'priority': ['video_learning', 'practice', 'recap'],
            'motivation': 'Wind down with some learning.'
        }
    }

    @staticmethod
    def get_learning_window(user: User):
        """Get the active learning window for a user"""
        pref = user.preferred_learning_time or 'morning'
        # Handle case variations
        pref = pref.lower().replace(' ', '_')
        if pref not in OrchestratorService.WINDOWS:
            pref = 'morning'
        return OrchestratorService.WINDOWS[pref]

    @staticmethod
    def is_in_learning_window(user: User, current_hour: int = None):
        """Check if user is currently in their preferred learning window"""
        if current_hour is None:
            current_hour = datetime.now().hour

        window = OrchestratorService.get_learning_window(user)
        start = window['start']
        end = window['end']

        # Handle crossing midnight (e.g. 19 to 1)
        if start < end:
            return start <= current_hour < end
        else:
            # Crosses midnight (e.g. 19 to 1) -> active if > 19 OR < 1
            return current_hour >= start or current_hour < end

    @staticmethod
    def should_notify(user: User, notification_type: str, urgency: str = 'normal') -> bool:
        """
        Decide whether to send a notification.
        Rules:
        - Critical: Always send.
        - Normal: Only send during learning window OR if user has 'Daily Reminders' ON (and it's reasonable time).
        - Marketing: Only if marketing_emails is True and in window.
        """
        if urgency == 'critical':
            return True

        # Check engagement toggles
        if notification_type == 'marketing' and not user.marketing_emails:
            return False
            
        if notification_type == 'daily_reminder' and not user.daily_reminders:
            return False

        # If User is in 'Deep Focus' mode, suppress ALL non-critical interruptions
        # unless it's the *start* of their window (handled by scheduled jobs, here we just check rule).
        # Actually deep focus might want BATCHED notifications (not implemented yet), 
        # so for now we enforce STRICT window.
        
        return OrchestratorService.is_in_learning_window(user)

    @staticmethod
    def get_ai_config(user: User):
        """Get AI persona configuration based on style and profile"""
        pref = user.preferred_learning_time or 'morning'
        pref = pref.lower().replace(' ', '_')
        
        config = OrchestratorService.AI_CONFIGS.get(pref, OrchestratorService.AI_CONFIGS['morning']).copy()
        
        # Override based on role if needed
        if user.user_role == 'student':
            config['tone'] += '_academic'
        
        return config

    @staticmethod
    def get_dashboard_greeting(user: User):
        """Get a context-aware greeting string"""
        config = OrchestratorService.get_ai_config(user)
        
        hour = datetime.now().hour
        if OrchestratorService.is_in_learning_window(user, hour):
            return f"Good to see you! You're in your prime {config['tone'].split('_')[0]} time."
        else:
            return f"Welcome back. {config['motivation']}"
