
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import User

app = create_app()

def debug_user(identifier):
    with app.app_context():
        print(f"--- Searching for: {identifier} ---")
        # Search by email (case insensitive search for debug)
        user_email = User.objects(email__iexact=identifier).first()
        # Search by mobile
        user_mobile = User.objects(mobile=identifier).first()
        
        if user_email:
            print(f"FOUND by Email ({user_email.email}):")
            print(f"  ID: {user_email.id}")
            print(f"  Mobile: {user_email.mobile}")
            print(f"  Status: {user_email.status}")
            print(f"  Verified: {user_email.is_verified}")
            print(f"  Email Verified: {getattr(user_email, 'is_email_verified', 'N/A')}")
            print(f"  Mobile Verified: {getattr(user_email, 'is_mobile_verified', 'N/A')}")
        else:
            print("NOT FOUND by Email (exact/iexact)")

        if user_mobile:
             print(f"FOUND by Mobile ({user_mobile.mobile}):")
             print(f"  ID: {user_mobile.id}") 
             
        # List all users to find collision
        print("\n--- ALL USERS IN DB ---")
        for u in User.objects():
            print(f"- {u.name} | {u.email} | {u.mobile} | Verified: {u.is_verified} | Status: {getattr(u, 'status', 'N/A')}")

if __name__ == "__main__":
    # Check both email and raw mobile if user provided one
    debug_user('shorajtomer@gmail.com')
