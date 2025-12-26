
import os
import sys
import bcrypt

# Add project root to path
sys.path.append(os.getcwd())

from app.models import User
from app.config import Config
from mongoengine import connect

def verify_legacy_fix():
    print("Connecting to DB...")
    connect(host=Config.MONGODB_SETTINGS['host'])
    
    email = "legacy_test_user@example.com"
    password = "secret_password_123"
    
    # Clean up potentially existing user
    User.objects(email=email).delete()
    
    print("Creating user with legacy BCrypt hash...")
    # Manual bcrypt hash generation
    # $2b$12$....
    legacy_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        name="Legacy Tester",
        email=email,
        mobile="9998887776",
        password_hash=legacy_hash
    )
    user.save()
    print(f"User saved with hash: {user.password_hash}")
    
    # Verify login (should trigger migration)
    print("Attempting check_password()...")
    fetched_user = User.objects(email=email).first()
    
    try:
        if fetched_user.check_password(password):
            print("✅ check_password returned True!")
        else:
            print("❌ check_password returned False!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ check_password raised exception: {e}")
        sys.exit(1)
        
    # Verify migration
    fetched_user.reload()
    print(f"New Hash after login: {fetched_user.password_hash}")
    
    if fetched_user.password_hash.startswith(('scrypt:', 'pbkdf2:')):
        print("✅ SUCCESS: Hash was migrated to Werkzeug format.")
    elif fetched_user.password_hash.startswith('$2b$'):
         print("❌ FAILURE: Hash was NOT migrated.")
    else:
         print(f"⚠️ UNKNOWN format: {fetched_user.password_hash}")
         
    # Cleanup
    fetched_user.delete()
    print("Test user deleted.")

if __name__ == "__main__":
    verify_legacy_fix()
