
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from app.models import User
from app.config import Config
from mongoengine import connect

def debug_user_hash(email):
    print(f"Connecting to DB: {Config.MONGODB_SETTINGS['host']}")
    connect(host=Config.MONGODB_SETTINGS['host'])
    
    user = User.objects(email=email).first()
    if not user:
        print(f"User {email} not found.")
        return

    print(f"User found: {user.name}")
    print(f"Hash length: {len(user.password_hash)}")
    print(f"Hash prefix: {user.password_hash[:20]}...")
    
    # Check if it looks like bcrypt
    if user.password_hash.startswith('$2b$'):
        print("Detected: Valid BCrypt prefix ($2b$)")
    elif user.password_hash.startswith('scrypt:'):
        print("Detected: Valid Werkzeug SCrypt prefix")
    elif user.password_hash.startswith('pbkdf2:'):
        print("Detected: Valid Werkzeug PBKDF2 prefix")
    else:
        print("Detected: Unknown prefix")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/debug_user_hash.py <email>")
    else:
        debug_user_hash(sys.argv[1])
