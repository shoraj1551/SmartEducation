"""
Data Migration Script for Learning Inbox Redesign
Migrates existing data to new status structure:
- 'dropped' → 'library'
- 'completed' → 'archived'
"""
from app.models import LearningItem
from mongoengine import connect
from app.config import Config

def migrate_learning_items():
    """Migrate learning items to new status structure"""
    
    print("Starting Learning Inbox data migration...")
    
    # Connect to MongoDB
    connect(host=Config.MONGODB_SETTINGS['host'])
    
    # Migrate 'dropped' items to 'library'
    dropped_items = LearningItem.objects(status='dropped')
    dropped_count = dropped_items.count()
    
    if dropped_count > 0:
        print(f"Found {dropped_count} items with status 'dropped'")
        dropped_items.update(status='library')
        print(f"✅ Migrated {dropped_count} dropped items to library")
    else:
        print("No dropped items found")
    
    # Migrate 'completed' items to 'archived'
    completed_items = LearningItem.objects(status='completed')
    completed_count = completed_items.count()
    
    if completed_count > 0:
        print(f"Found {completed_count} items with status 'completed'")
        completed_items.update(status='archived')
        print(f"✅ Migrated {completed_count} completed items to archived")
    else:
        print("No completed items found")
    
    # Summary
    total_migrated = dropped_count + completed_count
    print(f"\n📊 Migration Summary:")
    print(f"   - Dropped → Library: {dropped_count}")
    print(f"   - Completed → Archived: {completed_count}")
    print(f"   - Total migrated: {total_migrated}")
    
    # Show current status distribution
    print(f"\n📈 Current Status Distribution:")
    for status in ['library', 'active', 'paused', 'archived']:
        count = LearningItem.objects(status=status).count()
        print(f"   - {status.capitalize()}: {count}")
    
    print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    migrate_learning_items()
