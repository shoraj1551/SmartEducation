
import sys
import os
import requests
import string
import random
import time
from datetime import datetime

# Setup path to access app modules for DB inspection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import User, OTP

# Configuration
BASE_URL = 'http://localhost:5000/api/auth'
EMAIL_DOMAIN = 'e2etest.com' # Use allowed domain instead of test.com if filtered

def generate_random_digits(length=10):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run_test():
    print(f"\n{'='*60}")
    print(f"🔐 E2E AUTHENTICATION TEST: Registration -> Verification -> Login")
    print(f"{'='*60}\n")
    
    # 1. SETUP TEST DATA
    rand_suffix = generate_random_string(6)
    name = f"Test User {rand_suffix}"
    email = f"user_{rand_suffix}@smarteducation.com" # Use verified allowed domain
    mobile = f"9{generate_random_digits(9)}" # 10 digit starting with 9
    password = "SecurePassword123!"
    
    print(f"📝 Test Data:")
    print(f"   Name: {name}")
    print(f"   Email: {email}")
    print(f"   Mobile: {mobile}")
    print(f"   Password: {password}")

    # 2. REGISTER
    print(f"\nStep 1: Registering User...")
    payload = {
        'name': name,
        'email': email,
        'mobile': mobile,
        'password': password
    }
    try:
        res = requests.post(f'{BASE_URL}/register', json=payload)
        data = res.json()
        
        if res.status_code != 201:
            print(f"❌ Registration Failed (Status {res.status_code}): {data}")
            return
        
        print(f"✅ Registration endpoint called successfully.")
        user_id = data.get('user_id')
        print(f"   User ID: {user_id}")
        
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return

    # 3. FETCH OTPs FROM DB (Simulation of checking email/SMS)
    print(f"\nStep 2: Fetching OTPs from Database (backend-door)...")
    app = create_app()
    with app.app_context():
        # Find user or temp ID logic? 
        # Wait, /register returns user_id, which corresponds to User or TempUser ID.
        # Let's find OTPs for this user_id
        time.sleep(1) # Wait for async operations if any
        
        otps = OTP.objects(user_id=user_id, is_used=False)
        email_otp = None
        mobile_otp = None
        
        for otp in otps:
            print(f"   Found OTP: Type={otp.otp_type}, Code={otp.otp_code}")
            if otp.otp_type == 'email':
                email_otp = otp.otp_code
            elif otp.otp_type == 'mobile':
                mobile_otp = otp.otp_code
        
        if not email_otp or not mobile_otp:
            print(f"❌ Failed to retrieve both OTPs from DB.")
            # Note: Current logic might allow one?
            # User requirement: "Dual OTP".
            if not email_otp and not mobile_otp:
                 print("FATAL: No OTPs found.")
                 return

    # 4. VERIFY OTP
    print(f"\nStep 3: Verifying OTPs...")
    v_payload = {
        'user_id': user_id,
        'email_otp': email_otp,
        'mobile_otp': mobile_otp
    }
    
    try:
        res = requests.post(f'{BASE_URL}/verify-otp', json=v_payload)
        data = res.json()
        
        if res.status_code != 200:
             print(f"❌ Verification Failed (Status {res.status_code}): {data}")
             return
        
        print(f"✅ User Verified Successfully.")
        print(f"   Response: {data.get('message')}")
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return

    # 5. LOGIN
    print(f"\nStep 4: Logging In...")
    l_payload = {
        'identifier': email,
        'password': password
    }
    
    try:
        res = requests.post(f'{BASE_URL}/login', json=l_payload)
        data = res.json()
        
        if res.status_code != 200:
             print(f"❌ Login Failed (Status {res.status_code}): {data}")
             return
             
        token = data.get('token')
        if not token:
             print(f"❌ Login successful but no token returned.")
             return
             
        print(f"✅ Login Successful!")
        print(f"   Token received: {token[:20]}...")
        
    except Exception as e:
         print(f"❌ Error during login: {e}")
         return

    # 6. VERIFY TOKEN / PROTECTED ROUTE
    print(f"\nStep 5: Accessing Protected Route (Verify Token)...")
    t_payload = {'token': token}
    try:
        res = requests.post(f'{BASE_URL}/verify-token', json=t_payload)
        data = res.json()
        
        if res.status_code == 200 and data.get('valid') is True:
            print(f"✅ Token is valid.")
            print(f"   User Context: {data.get('user', {}).get('email')}")
        else:
             print(f"❌ Token verification failed: {data}")
             return
             
    except Exception as e:
        print(f"❌ Error verifying token: {e}")
        return

    print(f"\n{'='*60}")
    print(f"🎉 SUCCESS: Full E2E Auth Flow Completed!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_test()
