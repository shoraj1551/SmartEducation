
import os
import sys
import pymongo
from urllib.parse import urlparse

def migrate_local_to_atlas():
    print("🚀 SmartEducation Database Migration Tool")
    print("=========================================")
    
    # 1. Local Connection
    print("\n1️⃣  Connecting to LOCAL database (localhost:27017)...")
    try:
        local_client = pymongo.MongoClient("mongodb://localhost:27017/")
        local_db = local_client["SmartEducation"]
        # Check connection
        local_client.admin.command('ping')
        print("   ✅ Connected to Local DB.")
    except Exception as e:
        print(f"   ❌ Failed to connect to local DB: {e}")
        return

    # 2. Remote Connection
    print("\n2️⃣  Enter your MongoDB Atlas Connection String:")
    print("   (Example: mongodb+srv://admin:pass@cluster.mongodb.net/?...)")
    remote_uri = input("   > ").strip()
    
    if not remote_uri:
        print("   ❌ No URI provided. Exiting.")
        return

    print("   Connecting to REMOTE Atlas database...")
    try:
        remote_client = pymongo.MongoClient(remote_uri)
        # Parse db name from URI or default to SmartEducation
        uri_path = urlparse(remote_uri).path
        remote_db_name = uri_path.lstrip('/') if uri_path and uri_path != '/' else 'SmartEducation'
        remote_db = remote_client[remote_db_name]
        
        # Check connection
        remote_client.admin.command('ping')
        print(f"   ✅ Connected to Remote DB: {remote_db_name}")
    except Exception as e:
        print(f"   ❌ Failed to connect to Remote DB: {e}")
        return

    # 3. Migration Loop
    print("\n3️⃣  Starting Migration...")
    
    # Get all collection names
    collections = local_db.list_collection_names()
    
    if not collections:
        print("   ⚠️  No collections found in local database 'SmartEducation'.")
        return

    for col_name in collections:
        if col_name.startswith('system.'): continue # Skip system collections
        
        print(f"\n   📂 Migrating collection: {col_name}")
        local_col = local_db[col_name]
        remote_col = remote_db[col_name]
        
        docs = list(local_col.find())
        count = len(docs)
        
        if count == 0:
            print("      (Skipping empty collection)")
            continue
            
        print(f"      Found {count} documents.")
        
        inserted = 0
        skipped = 0
        
        for doc in docs:
            try:
                # Try to insert. If ID exists, we catch DuplicateKeyError
                remote_col.insert_one(doc)
                inserted += 1
            except pymongo.errors.DuplicateKeyError:
                # Optional: Update existing? For now, we skip to be safe/idempotent
                skipped += 1
            except Exception as e:
                print(f"      ❌ Error migrating doc {doc.get('_id')}: {e}")
                
        print(f"      ✅ Migrated: {inserted} | Skipped (Exists): {skipped}")

    print("\n=========================================")
    print("🎉 Migration Complete!")
    print("   You can now verify your data in MongoDB Atlas.")

if __name__ == "__main__":
    # Install pymongo if missing (though requirements.txt has it)
    try:
        import pymongo
    except ImportError:
        print("Installing pymongo...")
        os.system(f"{sys.executable} -m pip install pymongo")
        import pymongo
        
    migrate_local_to_atlas()
