
"""
Gamification Service (Feature 9)
Manages the Dopamine Layer: XP, Levels, and Badges.
Includes Phase 28 Architecture Improvements (Weekly Seasons).
"""
from app.models import User
import math
from datetime import datetime, timedelta

class GamificationService:
    
    BASE_XP = 500 # XP required for Level 2 (User starts at Lvl 1 with 0)
    
    @staticmethod
    def calculate_level(total_xp):
        """
        Calculate level based on total XP.
        Formula: Level = 1 + sqrt(XP / 500)
        """
        if total_xp < 0: return 1
        return 1 + int(math.sqrt(total_xp / 500))
        
    @staticmethod
    def calculate_xp_for_next_level(current_level):
        """
        Calculate XP needed to reach next level.
        Formula: XP = 500 * (Level - 1)^2
        """
        next_level = current_level + 1
        return 500 * ((next_level - 1) ** 2)
    
    @staticmethod
    def check_and_reset_weekly(user):
        """
        Check if we have crossed into a new week (Monday 00:00 UTC).
        If so, reset weekly_xp and update reset timestamp.
        """
        now = datetime.utcnow()
        last_reset = user.last_weekly_reset or user.created_at
        
        # Calculate start of current week (Monday)
        days_since_monday = now.weekday()
        start_of_week = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # If last reset was before this week's start, RESET.
        if last_reset < start_of_week:
            print(f"Resetting User {user.name} for New Season")
            user.weekly_xp = 0
            user.last_weekly_reset = now
            return True
        return False

    @staticmethod
    def award_xp(user_id, amount, source="System"):
        """
        Award XP to a user and check for level up.
        Updates both Lifetime XP and Weekly XP.
        """
        try:
            user = User.objects.get(id=user_id)
            
            # Check for weekly reset BEFORE adding points
            GamificationService.check_and_reset_weekly(user)

            old_level = user.level
            
            # Update Points
            user.xp_total += amount
            user.weekly_xp += amount # Phase 28: Add to weekly bucket
            
            # Check Level Up
            new_level = GamificationService.calculate_level(user.xp_total)
            
            leveled_up = False
            if new_level > old_level:
                user.level = new_level
                leveled_up = True
                
            user.save()
            
            return {
                'success': True,
                'leveled_up': leveled_up,
                'new_level': new_level,
                'xp_gained': amount,
                'total_xp': user.xp_total,
                'weekly_xp': user.weekly_xp,
                'level_title': GamificationService.get_level_title(new_level)
            }
        except Exception as e:
            print(f"Gamification Error: {e}")
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_progress(user_id):
        """Get full progress stats for UI"""
        user = User.objects.get(id=user_id)
        
        # Check reset on read (lazy evaluation)
        if GamificationService.check_and_reset_weekly(user):
            user.save()

        current_level = user.level
        next_level_xp = GamificationService.calculate_xp_for_next_level(current_level)
        prev_level_xp = 500 * ((current_level - 1) ** 2) if current_level > 1 else 0
        
        # XP within this level
        xp_in_level = user.xp_total - prev_level_xp
        xp_needed_for_level = next_level_xp - prev_level_xp
        
        progress_percent = int((xp_in_level / xp_needed_for_level) * 100) if xp_needed_for_level > 0 else 100
        
        return {
            'level': current_level,
            'title': GamificationService.get_level_title(current_level),
            'total_xp': user.xp_total,
            'weekly_xp': user.weekly_xp, # Phase 28
            'current_level_xp': xp_in_level,
            'next_level_xp_target': xp_needed_for_level,
            'percent': min(100, max(0, progress_percent)),
            'badges': user.badges
        }

    @staticmethod
    def get_level_title(level):
        """RPG Titles based on level"""
        titles = [
            (1, "Novice"),
            (5, "Apprentice"),
            (10, "Scholar"),
            (20, "Expert"),
            (30, "Master"),
            (40, "Grandmaster"),
            (50, "Legend"),
            (100, "God Tier")
        ]
        # Find highest title <= level
        current_title = "Novice"
        for thr, title in titles:
            if level >= thr:
                current_title = title
            else:
                break
        return current_title
