import unittest
from app.models import User
from werkzeug.security import generate_password_hash

class TestUserPassword(unittest.TestCase):
    def test_password_hashing(self):
        u = User(name="Test", email="test@example.com", mobile="1234567890")
        u.set_password("secret")
        # werkzeug default method is usually scrypt or pbkdf2
        hash_val = u.password_hash
        self.assertTrue(hash_val.startswith('scrypt:') or hash_val.startswith('pbkdf2:'), f"Unexpected hash format: {hash_val}")
        self.assertTrue(u.check_password("secret"))
        self.assertFalse(u.check_password("wrong"))

    def test_password_history(self):
        u = User(name="Test Hist", email="hist@example.com", mobile="0987654321")
        # Simulating history
        p1 = generate_password_hash("pass1")
        p2 = generate_password_hash("pass2")
        p3 = generate_password_hash("pass3")
        p4 = generate_password_hash("pass4")
        
        u.add_to_password_history(p1)
        u.add_to_password_history(p2)
        u.add_to_password_history(p3)
        self.assertEqual(len(u.password_history), 3)
        
        u.add_to_password_history(p4)
        self.assertEqual(len(u.password_history), 3)
        self.assertIn(p4, u.password_history)
        self.assertNotIn(p1, u.password_history)
        
        # Test check_password_in_history
        self.assertTrue(u.check_password_in_history("pass4"))
        self.assertTrue(u.check_password_in_history("pass3"))
        self.assertTrue(u.check_password_in_history("pass2"))
        self.assertFalse(u.check_password_in_history("pass1")) # Expired from history
        self.assertFalse(u.check_password_in_history("pass99"))

if __name__ == '__main__':
    unittest.main()
