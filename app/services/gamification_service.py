
"""
Gamification Service (Feature 9)
Manages the Dopamine Layer: XP, Levels, and Badges.
"""
from app.models import User
import math

class GamificationService:
    
    BASE_XP = 500 # XP required for Level 2 (User starts at Lvl 1 with 0)
    
    @staticmethod
    def calculate_level(total_xp):
        """
        Calculate level based on total XP.
        Formula: Level = 1 + sqrt(XP / 500)
        Ex: 0 XP -> Lvl 1
        500 XP -> Lvl 2
        2000 XP -> Lvl 3
        4500 XP -> Lvl 4
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
    def award_xp(user_id, amount, source="System"):
        """
        Award XP to a user and check for level up.
        Returns: { 'leveled_up': bool, 'new_level': int, 'xp_gained': int }
        """
        try:
            user = User.objects.get(id=user_id)
            old_level = user.level
            
            user.xp_total += amount
            new_level = GamificationService.calculate_level(user.xp_total)
            
            leveled_up = False
            if new_level > old_level:
                user.level = new_level
                leveled_up = True
                # TODO: Trigger notification or badge?
                
            user.save()
            
            return {
                'success': True,
                'leveled_up': leveled_up,
                'new_level': new_level,
                'xp_gained': amount,
                'total_xp': user.xp_total,
                'level_title': GamificationService.get_level_title(new_level)
            }
        except Exception as e:
            print(f"Gamification Error: {e}")
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_progress(user_id):
        """Get full progress stats for UI"""
        user = User.objects.get(id=user_id)
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
