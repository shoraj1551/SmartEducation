
import sys
import os
from datetime import datetime, timedelta

# Add app context
sys.path.append(os.getcwd())
from app import create_app
from app.models import Schedule, User

app = create_app()

with app.app_context():
    print("--- FIXING SCHEDULES ---")
    # specific user
    user = User.objects(email="shorajtomer@gmail.com").first()
    if not user:
        print("User not found")
        sys.exit(1)
        
    schedules = Schedule.objects(user_id=user)
    count = 0
    for s in schedules:
        # Check if it looks like a "Local as UTC" error
        # If created_at is close to start_time but offset is weird? 
        # Just blind fix: Shift from 18:10 (naive/bad UTC) to 12:40 (Real UTC for 18:10 IST)
        # Difference is 5.5 hours.
        # 18:10 - 5.5h = 12:40.
        
        # Only fix the one at 18:10
        if s.start_time.hour == 18 and s.start_time.minute == 10:
            print(f"Fixing event: {s.title} ({s.start_time})")
            s.start_time = s.start_time - timedelta(hours=5, minutes=30)
            if s.end_time:
                s.end_time = s.end_time - timedelta(hours=5, minutes=30)
            s.save()
            print(f"  -> New time: {s.start_time}")
            count += 1
            
    print(f"Fixed {count} events.")
