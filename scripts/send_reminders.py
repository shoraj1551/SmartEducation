
"""
Script to send daily reminder emails
Run this via cron or Task Scheduler: 0 9 * * * python scripts/send_reminders.py
"""
import sys
import os
import random

# Add parent dir to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import User
from app.services.otp_service import mail
from flask_mail import Message
from datetime import datetime

app = create_app()

REMINDER_TEMPLATES = [
    "Rise and shine! The world is built by those who show up. Time to learn.",
    "Consistency is key. 15 minutes today is better than 0 minutes.",
    "Your future self will thank you for the focus you put in today.",
    "Small steps every day add up to big results. Let's get started.",
    "The best time to plant a tree was 20 years ago. The second best time is now."
]

def send_daily_reminders():
    with app.app_context():
        # Find users who want reminders
        users = User.objects(daily_reminders=True)
        print(f"[{datetime.now()}] Found {users.count()} users with daily reminders enabled.")
        
        count = 0
        for user in users:
            try:
                # Basic check to avoid spamming if multiple runs? 
                # Ideally we track 'last_reminded_at' in DB, but for MVP we assume cron runs once.
                
                msg = Message(
                    subject="🚀 Daily Learning Motivation",
                    recipients=[user.email],
                    html=f"""
                    <div style="font-family: Arial; padding: 20px; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px;">
                        <h2 style="color: #667eea;">Good Morning, {user.name.split(' ')[0]}!</h2>
                        <p style="font-size: 16px; color: #555;">"{random.choice(REMINDER_TEMPLATES)}"</p>
                        
                        <div style="margin: 30px 0; text-align: center;">
                            <a href="http://localhost:5000/dashboard" 
                               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                      color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Open Dashboard
                            </a>
                        </div>
                        
                        <p style="font-size: 12px; color: #999;">
                            You are receiving this because you enabled Daily Reminders. 
                            <a href="http://localhost:5000/preferences">Unsubscribe</a>
                        </p>
                    </div>
                    """
                )
                mail.send(msg)
                print(f"✅ Sent to {user.email}")
                count += 1
            except Exception as e:
                print(f"❌ Failed to send to {user.email}: {e}")
        
        print(f"[{datetime.now()}] Job complete. Sent {count} emails.")

if __name__ == "__main__":
    send_daily_reminders()
