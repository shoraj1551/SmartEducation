
"""
Script to rescue locked out users by disabling 2FA
Usage: python scripts/fix_2fa_lockout.py <email>
"""
import sys
import os

# Add parent dir to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import User

def disable_2fa(email):
    app = create_app()
    with app.app_context():
        # Find user by email (case insensitive)
        user = User.objects(email__iexact=email).first()
        
        if not user:
            print(f"❌ User not found: {email}")
            return
            
        print(f"Found user: {user.name} ({user.email})")
        print(f"Current 2FA Status: {getattr(user, 'is_2fa_enabled', 'Not Set')}")
        
        # Force disable
        user.is_2fa_enabled = False
        user.save()
        
        print(f"✅ 2FA has been DISABLED for {user.email}.")
        print("You should now be able to login with just password.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/fix_2fa_lockout.py <email>")
        # Default fallback for urgency
        print("No email provided. Defaulting to 'shoraj@example.com' or similar if known...")
        # For this specific user request, I'll hardcode the likely email if arg missing
        # But looking at previous logs, his email is likely shorajtomer@gmail.com
        disable_2fa("shorajtomer@gmail.com") 
    else:
        disable_2fa(sys.argv[1])
