
import sys
import os
from datetime import datetime

# Add app context
sys.path.append(os.getcwd())
from app import create_app
from app.models import Schedule, User

app = create_app()

with app.app_context():
    print("--- DEBUGGING SCHEDULES ---")
    users = User.objects()
    print(f"Found {len(users)} users.")
    
    for user in users:
        print(f"\nUser: {user.email} (ID: {user.id})")
        schedules = Schedule.objects(user_id=user).order_by('-created_at')
        print(f"Found {len(schedules)} schedules.")
        
        for s in schedules[:5]: # Show last 5
            print(f"  - Title: {s.title}")
            print(f"    Start Time: {s.start_time} (iso: {s.start_time.isoformat()})")
            print(f"    Created At: {s.created_at}")
            print("-" * 30)
