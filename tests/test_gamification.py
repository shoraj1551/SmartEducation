
"""
Test Gamification Service (Feature 9)
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.gamification_service import GamificationService
import unittest

class TestGamification(unittest.TestCase):
    
    def test_level_calculation(self):
        # Lvl 1: 0 XP
        self.assertEqual(GamificationService.calculate_level(0), 1)
        # Lvl 2: 500 XP
        self.assertEqual(GamificationService.calculate_level(500), 2)
        # Lvl 3: 1 + sqrt(2000/500) = 1 + sqrt(4) = 3
        self.assertEqual(GamificationService.calculate_level(2000), 3)
        # Lvl 10: 1 + sqrt(XP/500). 9 = sqrt(XP/500). 81 * 500 = 40500 XP
        
    def test_next_level_target(self):
        # Lvl 1 -> 2 needs 500 XP. 
        # Formula: 500 * (2-1)^2 = 500. Correct.
        self.assertEqual(GamificationService.calculate_xp_for_next_level(1), 500)
        # Lvl 2 -> 3 needs 2000 total.
        # Formula: 500 * (3-1)^2 = 500 * 4 = 2000. Correct.
        self.assertEqual(GamificationService.calculate_xp_for_next_level(2), 2000)

if __name__ == '__main__':
    unittest.main()
