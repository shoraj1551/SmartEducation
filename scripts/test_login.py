import os, sys
sys.path.append(os.path.abspath('.'))
from app import create_app
from app.services.auth_service import AuthService

app = create_app()
# Use test user credentials created earlier
identifier = 'tester@e2e.com'
password = 'Password123!'

with app.app_context():
    user_data, msg = AuthService.login_user(identifier, password)
    print('Login message:', msg)
    print('Returned data:', user_data)
