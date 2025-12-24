
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import User

app = create_app()

def cleanup_db():
    with app.app_context():
        print("--- CLEANING UP DB ---")
        # Remove specific test users that might cause collision
        emails_to_remove = ['testuser06@gmail.com', 'qa@test.com']
        
        for email in emails_to_remove:
            user = User.objects(email=email).first()
            if user:
                print(f"Deleting user: {user.name} ({user.email})")
                user.delete()
            else:
                print(f"User {email} not found (already clean).")
        
        print("Cleanup complete.")

if __name__ == "__main__":
    cleanup_db()
