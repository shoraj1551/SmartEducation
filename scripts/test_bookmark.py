import os, sys
sys.path.append(os.path.abspath('.'))
from app import create_app
from app.services.bookmark_service import BookmarkService
from app.services.auth_service import AuthService

app = create_app()

with app.app_context():
    # login to get token and user data
    identifier = 'tester@e2e.com'
    password = 'Password123!'
    user_data, msg = AuthService.login_user(identifier, password)
    print('Login message:', msg)
    print('User data keys:', user_data.keys())

    # Use user id from user_data
    user_id = user_data['user']['id']

    # Add a bookmark
    bookmark, message = BookmarkService.add_bookmark(
        user_id,
        'https://en.wikipedia.org/wiki/Artificial_intelligence',
        'AI Wiki',
        'Test bookmark description',
        ['ai', 'ml']
    )
    print('Add bookmark result:', message)
    if bookmark:
        print('Bookmark dict:', bookmark.to_dict())
    else:
        print('Error adding bookmark')
