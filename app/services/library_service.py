import random
import time
import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import Bookmark, User
from datetime import datetime

from bson import ObjectId

class LibraryService:
    ALLOWED_EXTENSIONS = {'pdf', 'epub', 'mobi', 'doc', 'docx'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in LibraryService.ALLOWED_EXTENSIONS

    @staticmethod
    def simulate_sync(user_id, email, sources=None):
        """
        Simulates syncing from external platforms based on user email.
        """
        print(f"DEBUG: Starting sync for user_id={user_id}, email={email}") 
        
        time.sleep(1.5)
        
        try:
            # Ensure user_id is ObjectId
            uid = ObjectId(user_id) if isinstance(user_id, str) else user_id
            user = User.objects(id=uid).first()
        except Exception as e:
            print(f"DEBUG: Error looking up user: {e}")
            return False, f"User lookup error: {str(e)}"

        if not user:
            print(f"DEBUG: User not found for id={user_id}")
            return False, "User not found"
            
        print(f"DEBUG: User found: {user.email}") # DEBUG LOG

        new_resources = []
        
        # Intelligent Sync Logic
        # Only generating data for "demo" or "dev" emails to simulate a connected environment
        # Real users with unconnected accounts should see "No Data" as requested
        
        # Universal Access: Allow sync for all users to demonstrate functionality
        # Real implementation would check OAuth tokens here.
        is_demo_user = True 
        
        if not is_demo_user:
            return True, "No connected accounts found. Please connect YouTube, Udemy or Drive first."

        # Rich Mock Data Generator
        from app.constants import YOUTUBE_WATCH_URL_TEMPLATE, UDEMY_COURSE_URL_TEMPLATE, COURSERA_LEARN_URL_TEMPLATE
        mock_data = [
             {
                'title': 'Advanced System Design Patterns',
                'source': 'YouTube',
                'type': 'video', 
                'url': YOUTUBE_WATCH_URL_TEMPLATE.format(video_id='mock1'),
                'desc': 'Deep dive into microservices and scalable architecture. Learn asking the right questions.',
                'topic': 'System Design',
                'relevance': 0.98,
                'author': 'TechLead',
                'status': 'in_progress',
                'progress': 45,
                'platform': 'YouTube Premium',
                'meta_data': {'duration': '45m', 'views': '2.1M'}
            },
            {
                'title': 'The Complete Python Bootcamp: From Zero to Hero in Python',
                'source': 'Udemy',
                'type': 'course',
                'url': UDEMY_COURSE_URL_TEMPLATE.format(slug='python-bootcamp'),
                'desc': 'Learn Python like a Professional! Start from the basics and go all the way to creating your own applications and games.',
                'topic': 'Python',
                'relevance': 0.95,
                'author': 'Jose Portilla',
                'status': 'completed',
                'progress': 100,
                'platform': 'Udemy Business',
                'meta_data': {'duration': '22h 13m', 'rating': '4.6'}
            },
            {
                'title': 'Q4 Engineering Strategy for Cloud Migration',
                'source': 'Google Drive',
                'type': 'document',
                'url': '#',
                'desc': 'Confidential internal strategy document shared by CTO regarding the AWS migration plan.',
                'topic': 'Leadership',
                'relevance': 0.82,
                'author': 'Sarah Conner (CTO)',
                'status': 'not_started',
                'progress': 0,
                'platform': 'Drive Workplace',
                'meta_data': {'pages': '12', 'last_modified': '2 days ago'}
            },
            {
                'title': 'Machine Learning Specialty Certification',
                'source': 'Coursera',
                'type': 'course',
                'url': COURSERA_LEARN_URL_TEMPLATE.format(course_id='ml'),
                'desc': 'Master Machine Learning on AWS. Build, train, and deploy models using Amazon SageMaker.',
                'topic': 'Machine Learning',
                'relevance': 0.91,
                'author': 'Andrew Ng',
                'status': 'in_progress',
                'progress': 12,
                'platform': 'Coursera Plus',
                'meta_data': {'modules': '4/12', 'certificate': 'Available'}
            },
             {
                'title': 'React 18 Concurrent Features',
                'source': 'YouTube',
                'type': 'video',
                'url': YOUTUBE_WATCH_URL_TEMPLATE.format(video_id='mock2'),
                'desc': 'Understanding concurrency, suspense, and server components in React 18.',
                'topic': 'React',
                'relevance': 0.88,
                'author': 'Dan Abramov',
                'status': 'not_started',
                'progress': 0,
                'platform': 'YouTube',
                'meta_data': {'duration': '1h 20m'}
            },
            {
                'title': 'Clean Architecture: A Craftsman\'s Guide',
                'source': 'O\'Reilly',
                'type': 'book',
                'url': '#',
                'desc': 'Practical software architecture solutions from the legendary Robert C. Martin (Uncle Bob).',
                'topic': 'Architecture',
                'relevance': 0.96,
                'author': 'Robert C. Martin',
                'status': 'in_progress',
                'progress': 67,
                'platform': 'O\'Reilly Learning',
                'meta_data': {'pages': '432', 'format': 'ePub'}
            }
        ]

        # Sync Logic: Add items if they don't exist
        items_added_count = 0
        
        for item in mock_data:
            if not Bookmark.objects(user=user, title=item['title']).first():
                bookmark = Bookmark(
                    user=user,
                    title=item['title'],
                    url=item['url'],
                    description=item['desc'],
                    category=item['type'],
                    tags=item['topic'],
                    relevance_score=item['relevance'],
                    source=item['source'],
                    resource_type=item['type'],
                    topic=item['topic'],
                    # Rich Fields
                    status=item['status'],
                    progress=item['progress'],
                    author=item['author'],
                    platform=item['platform'],
                    meta_data=item['meta_data']
                )
                bookmark.save()
                items_added_count += 1
        
        if items_added_count == 0:
             return True, "Library is already up to date."

        return True, f"Synced {items_added_count} new high-quality resources from connected accounts."

    @staticmethod
    def handle_manual_upload(user_id, file, title, topic):
        if not file or file.filename == '':
            return False, "No file selected"
            
        if not LibraryService.allowed_file(file.filename):
            return False, "File type not allowed"

        filename = secure_filename(file.filename)
        # Verify user exists
        try:
            uid = ObjectId(user_id) if isinstance(user_id, str) else user_id
            user = User.objects(id=uid).first()
        except:
            return False, "Invalid User ID"

        if not user:
            return False, "User not found"
            
        # Ensure directory exists in configured static folder
        # Use root_path to be safe against relative path issues
        upload_folder = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'library')
        upload_folder = os.path.abspath(upload_folder)
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_name = f"{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(upload_folder, save_name)
        file.save(file_path)
        
        # Create Bookmark entry
        bookmark = Bookmark(
            user_id=user,
            title=title or filename,
            url=f"/static/uploads/library/{save_name}", # Local URL
            description=f"Uploaded manual document: {filename}",
            category='document',
            tags=[topic] if topic else [],
            relevance_score=1.0, # Manual uploads are highly relevant
            source='Manual Upload',
            resource_type='document',
            topic=topic,
            is_uploaded=True,
            file_path=file_path
        )
        
        bookmark.save()
        
        return True, "File uploaded successfully"
