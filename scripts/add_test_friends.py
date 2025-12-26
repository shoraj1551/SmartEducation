"""
Script to add test friends for shorajtomer@gmail.com
Creates 2 test users and establishes pod connections
"""
from app.models import User
from app.services.accountability_service import AccountabilityService
from mongoengine import connect
from datetime import datetime
import os

# Connect to MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/smarteducation')
connect(host=MONGODB_URI)

def create_test_friends():
    # Find the main user
    main_user = User.objects(email='shorajtomer@gmail.com').first()
    
    if not main_user:
        print("❌ User shorajtomer@gmail.com not found!")
        return
    
    print(f"✅ Found main user: {main_user.name} ({main_user.email})")
    
    # Create Test Friend 1
    friend1_email = 'alice.johnson@test.com'
    friend1 = User.objects(email=friend1_email).first()
    
    if not friend1:
        friend1 = User(
            name='Alice Johnson',
            email=friend1_email,
            is_verified=True,
            level=7,
            xp_total=3500,
            created_at=datetime.utcnow()
        )
        friend1.set_password('Test123!')
        friend1.save()
        print(f"✅ Created test friend 1: {friend1.name}")
    else:
        print(f"✅ Test friend 1 already exists: {friend1.name}")
    
    # Create Test Friend 2
    friend2_email = 'bob.smith@test.com'
    friend2 = User.objects(email=friend2_email).first()
    
    if not friend2:
        friend2 = User(
            name='Bob Smith',
            email=friend2_email,
            is_verified=True,
            level=5,
            xp_total=2100,
            created_at=datetime.utcnow()
        )
        friend2.set_password('Test123!')
        friend2.save()
        print(f"✅ Created test friend 2: {friend2.name}")
    else:
        print(f"✅ Test friend 2 already exists: {friend2.name}")
    
    # Check if AccountabilityPartner model exists
    try:
        from app.models import AccountabilityPartner
        
        # Create bidirectional pod connections
        # Connection 1: Main User <-> Friend 1
        partner1_main = AccountabilityPartner.objects(
            user_id=main_user.id,
            partner_email=friend1_email
        ).first()
        
        if not partner1_main:
            partner1_main = AccountabilityPartner(
                user_id=main_user,
                partner_email=friend1_email,
                partner_user_id=friend1,
                status='active',
                accepted_at=datetime.utcnow()
            )
            partner1_main.save()
            print(f"✅ Created pod connection: {main_user.name} -> {friend1.name}")
        
        partner1_reverse = AccountabilityPartner.objects(
            user_id=friend1.id,
            partner_email=main_user.email
        ).first()
        
        if not partner1_reverse:
            partner1_reverse = AccountabilityPartner(
                user_id=friend1,
                partner_email=main_user.email,
                partner_user_id=main_user,
                status='active',
                accepted_at=datetime.utcnow()
            )
            partner1_reverse.save()
            print(f"✅ Created reverse pod connection: {friend1.name} -> {main_user.name}")
        
        # Connection 2: Main User <-> Friend 2
        partner2_main = AccountabilityPartner.objects(
            user_id=main_user.id,
            partner_email=friend2_email
        ).first()
        
        if not partner2_main:
            partner2_main = AccountabilityPartner(
                user_id=main_user,
                partner_email=friend2_email,
                partner_user_id=friend2,
                status='active',
                accepted_at=datetime.utcnow()
            )
            partner2_main.save()
            print(f"✅ Created pod connection: {main_user.name} -> {friend2.name}")
        
        partner2_reverse = AccountabilityPartner.objects(
            user_id=friend2.id,
            partner_email=main_user.email
        ).first()
        
        if not partner2_reverse:
            partner2_reverse = AccountabilityPartner(
                user_id=friend2,
                partner_email=main_user.email,
                partner_user_id=main_user,
                status='active',
                accepted_at=datetime.utcnow()
            )
            partner2_reverse.save()
            print(f"✅ Created reverse pod connection: {friend2.name} -> {main_user.name}")
        
        print("\n🎉 Test pod setup complete!")
        print(f"\n📊 Your pod now has {len([partner1_main, partner2_main])} friends:")
        print(f"   1. {friend1.name} (Level {friend1.level}, {friend1.xp_total} XP)")
        print(f"   2. {friend2.name} (Level {friend2.level}, {friend2.xp_total} XP)")
        
    except ImportError:
        print("⚠️ AccountabilityPartner model not found in app.models")
        print("Creating connections using AccountabilityService...")
        
        # Use the service to create invites and accept them
        try:
            # Send invites
            AccountabilityService.send_invite(str(main_user.id), friend1_email)
            print(f"✅ Sent invite to {friend1.name}")
            
            AccountabilityService.send_invite(str(main_user.id), friend2_email)
            print(f"✅ Sent invite to {friend2.name}")
            
            print("\n⚠️ Note: Invites are pending. Friends need to accept them.")
            print("You can manually accept them through the Pods page or run accept script.")
            
        except Exception as e:
            print(f"❌ Error creating invites: {e}")

if __name__ == '__main__':
    create_test_friends()
