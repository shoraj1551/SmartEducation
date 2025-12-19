"""
Achievement service for SmartEducation gamification
"""
from models import User, Achievement, UserAchievement, Activity
from services.activity_service import ActivityService
import json

class AchievementService:
    @staticmethod
    def get_user_achievements(user_id):
        """Get all achievements earned by a user"""
        return UserAchievement.objects(user_id=user_id)

    @staticmethod
    def get_all_achievements():
        """Get all possible achievements"""
        return Achievement.objects()

    @staticmethod
    def award_achievement(user, achievement_code):
        """Award an achievement to a user if they haven't earned it yet"""
        existing = UserAchievement.objects(user_id=user.id, achievement_code=achievement_code).first()
        if existing:
            return False
            
        achievement = Achievement.objects(code=achievement_code).first()
        if not achievement:
            return False
            
        # Award XP
        user.xp_total += achievement.xp_reward
        
        # Check for Level Up
        next_level_xp = user.level * 1000
        if user.xp_total >= next_level_xp:
            user.level += 1
            ActivityService.log_activity(user.id, 'level_up', f'User reached level {user.level}')
            
        user.save()
        
        # Record Achievement
        ua = UserAchievement(user_id=user, achievement_code=achievement_code)
        ua.save()
        
        # Log Activity
        ActivityService.log_activity(user.id, 'achievement_earned', f'Earned badge: {achievement.title}')
        
        return True

    @staticmethod
    def check_milestones(user):
        """Check and award any pending milestones based on user stats/activity"""
        awarded = []
        
        # 1. First Bookmark
        from models import Bookmark
        if Bookmark.objects(user_id=user.id).count() >= 1:
            if AchievementService.award_achievement(user, 'first_bookmark'):
                awarded.append('first_bookmark')
                
        # 2. Profile Complete
        if user.bio and user.job_title and user.education_info:
             if AchievementService.award_achievement(user, 'profile_complete'):
                awarded.append('profile_complete')
                
        # 3. Momentum (Activity check)
        # Simplified: Check if user has > 5 activities
        if Activity.objects(user_id=user.id).count() >= 5:
            if AchievementService.award_achievement(user, 'consistent'):
                awarded.append('consistent')
                
        return awarded

    @staticmethod
    def initialize_achievements():
        """Seed the database with default achievements"""
        defaults = [
            {'code': 'first_bookmark', 'title': 'Knowledge Seeker', 'description': 'Saved your first educational resource.', 'xp_reward': 50, 'icon': 'fa-bookmark'},
            {'code': 'profile_complete', 'title': 'Verified Identity', 'description': 'Completed your 100% verified profile.', 'xp_reward': 100, 'icon': 'fa-id-card'},
            {'code': 'consistent', 'title': 'Momentum', 'description': 'Maintained a strong activity streak.', 'xp_reward': 150, 'icon': 'fa-fire'}
        ]
        
        for d in defaults:
            if not Achievement.objects(code=d['code']).first():
                Achievement(**d).save()
