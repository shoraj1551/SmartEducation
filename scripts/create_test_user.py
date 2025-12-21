import os
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect
from app.models import User

def create_test_user():
    load_dotenv()
    host = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/SmartEducation')
    connect(host=host)
    
    email = 'tester@e2e.com'
    mobile = '9999999999'
    
    # Check if user already exists
    user = User.objects(email=email).first()
    if user:
        print(f"User {email} already exists. Updating...")
    else:
        print(f"Creating new user {email}...")
        user = User(email=email, mobile=mobile)
        
    user.name = 'E2E Tester'
    user.password_hash = bcrypt.hashpw('Password123!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.is_verified = True
    user.updated_at = datetime.utcnow()
    user.save()
    print(f"User {email} created/updated and verified successfully!")

if __name__ == '__main__':
    create_test_user()
