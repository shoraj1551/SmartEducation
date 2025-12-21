"""
Priority Service for Feature 4: Smart Priority Engine
Handles multi-factor priority calculation and ranking
"""
from datetime import datetime, timedelta
from app.models import LearningItem, User, DailyTask
from mongoengine.errors import DoesNotExist
import math


class PriorityService:
    """Service for calculating and managing learning item priorities"""
    
    # Priority factor weights
    WEIGHT_DEADLINE_URGENCY = 0.40
    WEIGHT_CAREER_RELEVANCE = 0.25
    WEIGHT_EFFORT_INVESTED = 0.20
    WEIGHT_DIFFICULTY_MATCH = 0.15
    
    # User skill levels
    SKILL_BEGINNER = 1
    SKILL_INTERMEDIATE = 2
    SKILL_ADVANCED = 3
    
    @staticmethod
    def calculate_priority_score(learning_item, user_profile=None):
        """
        Calculate priority score for a learning item
        
        Priority Score = 
          (0.4 × Deadline Urgency) +
          (0.25 × Career Relevance) +
          (0.2 × Effort Invested) +
          (0.15 × Difficulty Match)
        
        Args:
            learning_item: LearningItem object
            user_profile: Optional user profile with goals and skill level
            
        Returns:
            Float priority score (0-100)
        """
        # Calculate each factor
        deadline_score = PriorityService._calculate_deadline_urgency(learning_item)
        career_score = PriorityService._calculate_career_relevance(learning_item, user_profile)
        effort_score = PriorityService._calculate_effort_invested(learning_item)
        difficulty_score = PriorityService._calculate_difficulty_match(learning_item, user_profile)
        
        # Weighted sum
        priority_score = (
            PriorityService.WEIGHT_DEADLINE_URGENCY * deadline_score +
            PriorityService.WEIGHT_CAREER_RELEVANCE * career_score +
            PriorityService.WEIGHT_EFFORT_INVESTED * effort_score +
            PriorityService.WEIGHT_DIFFICULTY_MATCH * difficulty_score
        )
        
        return round(priority_score, 2)
    
    @staticmethod
    def _calculate_deadline_urgency(item):
        """
        Calculate deadline urgency score (0-100)
        Higher score = more urgent
        """
        if not item.target_completion_date:
            return 50.0  # Medium urgency if no deadline
        
        days_until_deadline = (item.target_completion_date - datetime.utcnow()).days
        
        if days_until_deadline < 0:
            return 100.0  # Overdue - maximum urgency
        elif days_until_deadline == 0:
            return 95.0  # Due today
        elif days_until_deadline <= 3:
            return 90.0  # Due within 3 days
        elif days_until_deadline <= 7:
            return 75.0  # Due within a week
        elif days_until_deadline <= 14:
            return 60.0  # Due within 2 weeks
        elif days_until_deadline <= 30:
            return 40.0  # Due within a month
        else:
            return 20.0  # More than a month away
    
    @staticmethod
    def _calculate_career_relevance(item, user_profile):
        """
        Calculate career relevance score (0-100)
        Based on alignment with user's career goals
        """
        if not user_profile or not hasattr(user_profile, 'career_goals'):
            return 50.0  # Default medium relevance
        
        # Check if item tags match user's career goals
        user_goals = user_profile.get('career_goals', [])
        item_tags = item.tags or []
        item_category = item.category or ''
        
        if not user_goals:
            return 50.0
        
        # Calculate overlap
        matching_tags = set(item_tags) & set(user_goals)
        category_match = any(goal.lower() in item_category.lower() for goal in user_goals)
        
        if len(matching_tags) >= 3 or category_match:
            return 90.0  # High relevance
        elif len(matching_tags) >= 2:
            return 75.0  # Good relevance
        elif len(matching_tags) >= 1:
            return 60.0  # Some relevance
        else:
            return 30.0  # Low relevance
    
    @staticmethod
    def _calculate_effort_invested(item):
        """
        Calculate effort invested score (0-100)
        Higher score = more effort already invested (sunk cost)
        """
        if item.total_duration == 0:
            return 0.0
        
        progress_percentage = item.progress_percentage
        
        # Sunk cost fallacy - prioritize items with significant progress
        if progress_percentage >= 75:
            return 95.0  # Almost done - high priority to finish
        elif progress_percentage >= 50:
            return 80.0  # Halfway - good priority
        elif progress_percentage >= 25:
            return 60.0  # Some progress
        elif progress_percentage >= 10:
            return 40.0  # Started
        else:
            return 20.0  # Just started
    
    @staticmethod
    def _calculate_difficulty_match(item, user_profile):
        """
        Calculate difficulty match score (0-100)
        Higher score = better match between content difficulty and user skill
        """
        if not user_profile or not hasattr(user_profile, 'skill_level'):
            return 50.0  # Default medium match
        
        user_level = user_profile.get('skill_level', PriorityService.SKILL_INTERMEDIATE)
        
        # Estimate content difficulty from metadata or category
        content_difficulty = PriorityService._estimate_content_difficulty(item)
        
        # Calculate match (perfect match = 100, complete mismatch = 0)
        level_difference = abs(user_level - content_difficulty)
        
        if level_difference == 0:
            return 100.0  # Perfect match
        elif level_difference == 1:
            return 70.0  # Close match
        else:
            return 40.0  # Mismatch
    
    @staticmethod
    def _estimate_content_difficulty(item):
        """Estimate content difficulty from item metadata"""
        # Check metadata for difficulty hints
        if item.metadata:
            if 'difficulty' in item.metadata:
                difficulty_map = {
                    'beginner': PriorityService.SKILL_BEGINNER,
                    'intermediate': PriorityService.SKILL_INTERMEDIATE,
                    'advanced': PriorityService.SKILL_ADVANCED
                }
                return difficulty_map.get(item.metadata['difficulty'].lower(), PriorityService.SKILL_INTERMEDIATE)
        
        # Estimate from category or title
        title_lower = item.title.lower()
        category_lower = (item.category or '').lower()
        
        if any(word in title_lower or word in category_lower for word in ['beginner', 'intro', 'basics', 'fundamentals']):
            return PriorityService.SKILL_BEGINNER
        elif any(word in title_lower or word in category_lower for word in ['advanced', 'expert', 'master', 'deep dive']):
            return PriorityService.SKILL_ADVANCED
        else:
            return PriorityService.SKILL_INTERMEDIATE
    
    @staticmethod
    def get_ranked_items(user_id, user_profile=None):
        """
        Get all active learning items ranked by priority
        
        Args:
            user_id: User ID
            user_profile: Optional user profile data
            
        Returns:
            List of items with priority scores, sorted by priority (highest first)
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        # Get active learning items
        items = LearningItem.objects(user_id=user, status='active')
        
        # Calculate priority for each item
        ranked_items = []
        for item in items:
            priority_score = PriorityService.calculate_priority_score(item, user_profile)
            
            # Update item's priority score
            item.priority_score = priority_score
            item.save()
            
            ranked_items.append({
                'item': item,
                'priority_score': priority_score,
                'breakdown': PriorityService._get_priority_breakdown(item, user_profile)
            })
        
        # Sort by priority (highest first)
        ranked_items.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return ranked_items
    
    @staticmethod
    def _get_priority_breakdown(item, user_profile):
        """Get detailed breakdown of priority calculation"""
        return {
            'deadline_urgency': PriorityService._calculate_deadline_urgency(item),
            'career_relevance': PriorityService._calculate_career_relevance(item, user_profile),
            'effort_invested': PriorityService._calculate_effort_invested(item),
            'difficulty_match': PriorityService._calculate_difficulty_match(item, user_profile)
        }
    
    @staticmethod
    def get_top_priority(user_id, user_profile=None):
        """
        Get the single highest priority item for today
        
        Args:
            user_id: User ID
            user_profile: Optional user profile data
            
        Returns:
            Dictionary with top priority item and explanation
        """
        ranked_items = PriorityService.get_ranked_items(user_id, user_profile)
        
        if not ranked_items:
            return None
        
        top_item = ranked_items[0]
        
        # Generate explanation
        explanation = PriorityService._generate_priority_explanation(
            top_item['item'],
            top_item['breakdown']
        )
        
        return {
            'item': top_item['item'].to_dict(),
            'priority_score': top_item['priority_score'],
            'breakdown': top_item['breakdown'],
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_priority_explanation(item, breakdown):
        """Generate human-readable explanation for why this item is top priority"""
        reasons = []
        
        # Deadline urgency
        if breakdown['deadline_urgency'] >= 90:
            reasons.append("⚠️ Deadline is very close or overdue")
        elif breakdown['deadline_urgency'] >= 75:
            reasons.append("📅 Due within a week")
        
        # Career relevance
        if breakdown['career_relevance'] >= 80:
            reasons.append("🎯 Highly relevant to your career goals")
        
        # Effort invested
        if breakdown['effort_invested'] >= 75:
            reasons.append("💪 You're already 50%+ complete - finish strong!")
        elif breakdown['effort_invested'] >= 50:
            reasons.append("📈 Good progress made - keep momentum")
        
        # Difficulty match
        if breakdown['difficulty_match'] >= 90:
            reasons.append("✨ Perfect match for your skill level")
        
        if not reasons:
            reasons.append("📚 Balanced priority across all factors")
        
        return reasons
    
    @staticmethod
    def record_feedback(user_id, item_id, feedback_type, feedback_data=None):
        """
        Record user feedback on priority suggestions
        
        Args:
            user_id: User ID
            item_id: Learning item ID
            feedback_type: 'agree', 'disagree', 'skip'
            feedback_data: Optional additional feedback data
            
        Returns:
            Feedback record
        """
        # Store feedback in item metadata for future algorithm improvements
        try:
            item = LearningItem.objects.get(id=item_id)
            
            if not item.metadata:
                item.metadata = {}
            
            if 'priority_feedback' not in item.metadata:
                item.metadata['priority_feedback'] = []
            
            item.metadata['priority_feedback'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'feedback_type': feedback_type,
                'feedback_data': feedback_data or {}
            })
            
            item.save()
            
            return {'success': True, 'message': 'Feedback recorded'}
        except DoesNotExist:
            return {'success': False, 'message': 'Item not found'}
