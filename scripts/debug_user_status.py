
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, OTP

app = create_app()

def check_user(email):
    with app.app_context():
        print(f"--- Debugging User: {email} ---")
        user = User.objects(email=email).first()
        
        if not user:
            print(f"❌ User not found with email: {email}")
            # Try mobile?
            return

        print(f"✅ User Found: {user.name} (ID: {user.id})")
        print(f"   Email: {user.email}")
        print(f"   Mobile: {user.mobile}")
        print(f"   Is Verified: {user.is_verified}")
        
        # Check status safely
        status = getattr(user, 'status', 'MISSING_FIELD')
        print(f"   Status: {status}")
        
        print(f"   Has Password Hash: {'Yes' if user.password_hash else 'No'}")
        
        # Check OTPs
        otps = OTP.objects(user_id=str(user.id))
        print(f"\n--- OTP Records ({otps.count()}) ---")
        for otp in otps:
            print(f"   Type: {otp.otp_type} | Code: {otp.otp_code} | Purpose: {otp.purpose} | Used: {otp.is_used} | Expired: {otp.is_expired()}")

        if user.is_verified and status != 'ACTIVE':
            print("\n⚠️  DIAGNOSIS: User is verified but status is NOT ACTIVE.")
            print("   Action: Run fix script or manual update.")
        elif not user.is_verified:
            print("\n⚠️  DIAGNOSIS: User is NOT verified.")
        else:
            print("\n✅ DIAGNOSIS: User record looks healthy. Issue might be password or frontend.")

if __name__ == "__main__":
    check_user('shorajtomer@gmail.com')
