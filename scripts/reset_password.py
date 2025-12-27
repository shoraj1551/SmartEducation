
import os
import pymongo
from dotenv import load_dotenv
import sys
from werkzeug.security import generate_password_hash

# Load .env manually
load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
    print("❌ MONGODB_URI not found in .env")
    sys.exit(1)

print(f"Connecting to DB...") 

try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users = db['users']
    
    email = "shorajtomer@gmail.com"
    new_pass = "Password123!"
    hashed_pass = generate_password_hash(new_pass)
    
    result = users.update_one(
        {"email": email},
        {"$set": {
            "password_hash": hashed_pass,
            "is_active": True
        }}
    )
    
    if result.modified_count > 0:
        print(f"✅ SUCCESSFULLY reset password for: {email}")
        print(f"   New Password: {new_pass}")
    else:
        print(f"⚠️  User found but no changes made (Password might be same?)")
        # Check if user actually exists
        if users.count_documents({"email": email}) == 0:
            print("❌ User DOES NOT EXIST. Cannot reset password.")

except Exception as e:
    print(f"❌ Error: {e}")
