
"""
Priority Service (Intelligence Engine)
Calculates dynamic priority scores for learning items based on Relevance, Urgency, and Effort.
"""
from datetime import datetime
from app.models import LearningItem, User

class PriorityService:
    @staticmethod
    def calculate_score(item):
        """
        Calculate priority score (0-100)
        
        Factors:
        1. Relevance (40%): Based on user goals vs content match (bookmark.relevance_score)
        2. Urgency (40%): Proximity to target_completion_date
        3. Effort (20%): Shorter items get a slight boost (quick wins)
        """
        
        # 1. Relevance Score (0-1.0) -> Scaled to 40
        # If imported from bookmark, it relies on that score. Default 0.5 if missing.
        relevance = item.priority_score if item.priority_score <= 1.0 else (item.priority_score / 100.0)
        start_relevance = max(0.1, min(relevance, 1.0))
        score_relevance = start_relevance * 40
        
        # 2. Urgency Score (0-1.0) -> Scaled to 40
        score_urgency = 0
        if item.target_completion_date:
            days_left = (item.target_completion_date - datetime.utcnow()).days
            if days_left <= 0:
                urgency = 1.0  # Overdue or due today
            elif days_left <= 7:
                urgency = 0.9  # Due this week
            elif days_left <= 14:
                urgency = 0.7
            elif days_left <= 30:
                urgency = 0.5
            else:
                urgency = 0.2
            score_urgency = urgency * 40
            
        # 3. Effort Score (0-1.0) -> Scaled to 20
        # "Quick Wins" logic: shorter duration = higher score preference
        score_effort = 10 # Default neutral
        if item.total_duration > 0:
            minutes = item.total_duration
            if minutes <= 30:
                score_effort = 20 # Easy
            elif minutes <= 60:
                score_effort = 15
            elif minutes <= 180:
                score_effort = 10 
            else:
                score_effort = 5 # Heavy
                
        final_score = score_relevance + score_urgency + score_effort
        return round(final_score, 1)

    @staticmethod
    def recalculate_for_user(user_id):
        """Recalculate priority scores for all active items of a user"""
        items = LearningItem.objects(user_id=user_id, status__ne='dropped')
        updated_count = 0
        
        for item in items:
            new_score = PriorityService.calculate_score(item)
            if new_score != item.priority_score:
                item.priority_score = new_score
                item.save()
                updated_count += 1
                
        return updated_count

    @staticmethod
    def get_top_priorities(user_id, limit=3):
        """Get the top N items sorted by calculated priority"""
        return LearningItem.objects(
            user_id=user_id, 
            status='active'
        ).order_by('-priority_score').limit(limit)
