"""
Flask shell commands for testing
Run with: flask shell
Then: from scripts.test_data import add_test_friends; add_test_friends()
"""

def add_test_friends():
    """Add test friends for shorajtomer@gmail.com"""
    from app.models import User, AccountabilityPartner
    from datetime import datetime
    
    # Find the main user
    main_user = User.objects(email='shorajtomer@gmail.com').first()
    
    if not main_user:
        print("❌ User shorajtomer@gmail.com not found!")
        print("Available users:")
        for u in User.objects.only('email', 'name'):
            print(f"  - {u.name} ({u.email})")
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
    else:
        print(f"✅ Pod connection already exists: {main_user.name} -> {friend1.name}")
    
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
    else:
        print(f"✅ Reverse pod connection already exists: {friend1.name} -> {main_user.name}")
    
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
    else:
        print(f"✅ Pod connection already exists: {main_user.name} -> {friend2.name}")
    
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
    else:
        print(f"✅ Reverse pod connection already exists: {friend2.name} -> {main_user.name}")
    
    print("\n🎉 Test pod setup complete!")
    print(f"\n📊 Your pod now has 2 friends:")
    print(f"   1. {friend1.name} (Level {friend1.level}, {friend1.xp_total} XP)")
    print(f"   2. {friend2.name} (Level {friend2.level}, {friend2.xp_total} XP)")
    print(f"\n✅ Login as shorajtomer@gmail.com and visit /pods to see your friends!")
    
    return {
        'main_user': main_user.name,
        'friends': [
            {'name': friend1.name, 'email': friend1.email, 'level': friend1.level},
            {'name': friend2.name, 'email': friend2.email, 'level': friend2.level}
        ]
    }
