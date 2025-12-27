
import os
import pymongo
from dotenv import load_dotenv
import sys

# Load .env manually since we are running as a script
load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
    print("❌ MONGODB_URI not found in .env")
    sys.exit(1)

print(f"Connecting to: {uri.split('@')[1]}") # Print host only for privacy

try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users = db['users']
    
    email = "shorajtomer@gmail.com"
    user = users.find_one({"email": email})
    
    if user:
        print(f"✅ User found: {user.get('email')}")
        print(f"   Name: {user.get('first_name')} {user.get('last_name')}")
        
        pwd = user.get('password')
        if pwd:
            print(f"   Password Hash: {pwd[:10]}... (Length: {len(pwd)})")
            if len(pwd) < 20: 
                print("   ⚠️ WARNING: Password hash looks suspiciously short!")
            if not pwd.startswith(('scrypt', 'pbkdf2', 'sha')):
                 print("   ℹ️ Note: Hash format validation skipped (custom format?)")
        else:
            print("   ❌ ERROR: Password field is MISSING or EMPTY!")
            
        print(f"   Is Active: {user.get('is_active', 'Not Set')}")
        print(f"   Roles: {user.get('roles', [])}")
        
    else:
        print(f"❌ User '{email}' NOT FOUND in connection '{db.name}'.")
        print("   Total users in DB:", users.count_documents({}))
        print("   Sample emails:", [u['email'] for u in users.find().limit(5)])

except Exception as e:
    print(f"❌ Connection Error: {e}")
