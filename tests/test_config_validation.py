import unittest
from unittest.mock import patch
import os
from app.config import Config

class TestConfigValidation(unittest.TestCase):
    def setUp(self):
        # Save original env vars
        self.original_env = os.environ.copy()

    def tearDown(self):
        # Restore original env vars
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch('app.config.Config.DEBUG', True)
    def test_validate_debug_mode(self):
        """Should verify that validation is skipped in debug mode (no output/error)."""
        # We can simulate missing vars by clearing env
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        
        # Should not raise or print warning (though print capture is harder here, no exception is key)
        try:
            Config.validate()
        except Exception as e:
            self.fail(f"Config.validate raised exception in DEBUG mode: {e}")

    @patch('app.config.Config.DEBUG', False)
    def test_validate_production_mode_missing_vars(self):
        """
        Should print warning if critical vars are missing in production. 
        Note: The implementation was changed to just print a warning, not raise.
        """
        # Ensure a critical var is missing
        if 'SECRET_KEY' in os.environ:
           del os.environ['SECRET_KEY']
        
        # We patch print to verify it was called
        with patch('builtins.print') as mock_print:
            Config.validate()
            # Verify that print was called with "Warning: Missing environment variables"
            args, _ = mock_print.call_args
            self.assertIn("Warning: Missing environment variables", args[0])

    @patch('app.config.Config.DEBUG', False)
    def test_validate_production_mode_all_vars_present(self):
        """Should pass without warning if all vars are present."""
        # Config values are loaded at import time, so mocking os.environ alone doesn't change
        # the class attributes 'SECRET_KEY', etc. We must patch the class attributes directly.
        with patch.multiple('app.config.Config',
                            SECRET_KEY='test_key',
                            JWT_SECRET_KEY='test_jwt',
                            MAIL_USERNAME='user',
                            MAIL_PASSWORD='pass',
                            TWILIO_ACCOUNT_SID='sid',
                            TWILIO_AUTH_TOKEN='token',
                            TWILIO_PHONE_NUMBER='123'):
            with patch('builtins.print') as mock_print:
                Config.validate()
                mock_print.assert_not_called()

if __name__ == '__main__':
    unittest.main()
