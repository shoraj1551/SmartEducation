import os, sys
sys.path.append(os.path.abspath('.'))

# Initialize Flask app to set up MongoDB connection
from app import create_app
app = create_app()

from app.models import User

# Fetch a user (example email)
user = User.objects(email='tester@e2e.com').first()
if user:
    print(f'User found: {user.email}')
    print(f'xp_total: {getattr(user, "xp_total", None)}')
    print(f'level: {getattr(user, "level", None)}')
else:
    print('User not found')
