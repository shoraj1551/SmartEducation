"""
Direct MongoDB script to add test friends
Run this with: python -m scripts.add_friends_direct
"""
if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from app import create_app
    from app.models import User, AccountabilityPartner
    from datetime import datetime
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Looking for main user...")
        main_user = User.objects(email='shorajtomer@gmail.com').first()
        
        if not main_user:
            print("❌ User shorajtomer@gmail.com not found!")
            print("\n📋 Available users:")
            for u in User.objects.only('email', 'name'):
                print(f"  - {u.name} ({u.email})")
            sys.exit(1)
        
        print(f"✅ Found: {main_user.name} ({main_user.email})")
        
        # Create Friend 1
        print("\n👤 Creating Friend 1...")
        friend1 = User.objects(email='alice.johnson@test.com').first()
        if not friend1:
            friend1 = User(
                name='Alice Johnson',
                email='alice.johnson@test.com',
                mobile='+1234567890',
                is_verified=True,
                level=7,
                xp_total=3500,
                created_at=datetime.utcnow()
            )
            friend1.set_password('Test123!')
            friend1.save()
            print(f"✅ Created: {friend1.name}")
        else:
            print(f"✅ Already exists: {friend1.name}")
        
        # Create Friend 2
        print("\n👤 Creating Friend 2...")
        friend2 = User.objects(email='bob.smith@test.com').first()
        if not friend2:
            friend2 = User(
                name='Bob Smith',
                email='bob.smith@test.com',
                mobile='+1234567891',
                is_verified=True,
                level=5,
                xp_total=2100,
                created_at=datetime.utcnow()
            )
            friend2.set_password('Test123!')
            friend2.save()
            print(f"✅ Created: {friend2.name}")
        else:
            print(f"✅ Already exists: {friend2.name}")
        
        # Create Pod Connections
        print("\n🔗 Creating pod connections...")
        
        # Main -> Friend1
        p1 = AccountabilityPartner.objects(user_id=main_user.id, partner_email='alice.johnson@test.com').first()
        if not p1:
            p1 = AccountabilityPartner(
                user_id=main_user,
                partner_email='alice.johnson@test.com',
                partner_user_id=friend1,
                status='active',
                accepted_at=datetime.utcnow()
            )
            p1.save()
            print(f"✅ {main_user.name} -> {friend1.name}")
        else:
            print(f"✅ Already connected: {main_user.name} -> {friend1.name}")
        
        # Friend1 -> Main
        p1r = AccountabilityPartner.objects(user_id=friend1.id, partner_email=main_user.email).first()
        if not p1r:
            p1r = AccountabilityPartner(
                user_id=friend1,
                partner_email=main_user.email,
                partner_user_id=main_user,
                status='active',
                accepted_at=datetime.utcnow()
            )
            p1r.save()
            print(f"✅ {friend1.name} -> {main_user.name}")
        else:
            print(f"✅ Already connected: {friend1.name} -> {main_user.name}")
        
        # Main -> Friend2
        p2 = AccountabilityPartner.objects(user_id=main_user.id, partner_email='bob.smith@test.com').first()
        if not p2:
            p2 = AccountabilityPartner(
                user_id=main_user,
                partner_email='bob.smith@test.com',
                partner_user_id=friend2,
                status='active',
                accepted_at=datetime.utcnow()
            )
            p2.save()
            print(f"✅ {main_user.name} -> {friend2.name}")
        else:
            print(f"✅ Already connected: {main_user.name} -> {friend2.name}")
        
        # Friend2 -> Main
        p2r = AccountabilityPartner.objects(user_id=friend2.id, partner_email=main_user.email).first()
        if not p2r:
            p2r = AccountabilityPartner(
                user_id=friend2,
                partner_email=main_user.email,
                partner_user_id=main_user,
                status='active',
                accepted_at=datetime.utcnow()
            )
            p2r.save()
            print(f"✅ {friend2.name} -> {main_user.name}")
        else:
            print(f"✅ Already connected: {friend2.name} -> {main_user.name}")
        
        print("\n🎉 SUCCESS! Test friends added!")
        print(f"\n📊 Your pod now has 2 friends:")
        print(f"   1. {friend1.name} - Level {friend1.level}, {friend1.xp_total} XP")
        print(f"   2. {friend2.name} - Level {friend2.level}, {friend2.xp_total} XP")
        print(f"\n✅ Refresh the /pods page to see them!")
