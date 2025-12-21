import random
import time
import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import Bookmark, User
from datetime import datetime

from bson import ObjectId

class LibraryService:
    # ... (constants)

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
        
        # Generator for mock items based on email prefix context (e.g., dev vs manager)
        is_dev = 'dev' in email.lower() or 'tech' in email.lower() or True
        
        mock_data = [
             {
                'title': 'Advanced System Design Patterns',
                'source': 'YouTube',
                'type': 'video', 
                'url': 'https://youtube.com/watch?v=mock1',
                'desc': 'Deep dive into microservices and scalable architecture.',
                'topic': 'System Design',
                'relevance': 0.95
            },
            {
                'title': 'The Complete Python Bootcamp',
                'source': 'Udemy',
                'type': 'course',
                'url': 'https://udemy.com/course/python-bootcamp',
                'desc': 'Zero to Hero in Python with real world projects.',
                'topic': 'Python',
                'relevance': 0.88
            },
            {
                'title': 'Q4 Engineering Strategy.pdf',
                'source': 'Google Drive',
                'type': 'document',
                'url': '#',
                'desc': 'Internal strategy document shared by CTO.',
                'topic': 'Leadership',
                'relevance': 0.75
            },
            {
                'title': 'Machine Learning Specialty',
                'source': 'Coursera',
                'type': 'course',
                'url': 'https://coursera.org/learn/ml',
                'desc': 'Official certification preparation course.',
                'topic': 'Machine Learning',
                'relevance': 0.92
            },
             {
                'title': 'React 18 Features Walkthrough',
                'source': 'YouTube',
                'type': 'video',
                'url': 'https://youtube.com/watch?v=mock2',
                'desc': 'Understanding concurrency and server components.',
                'topic': 'React',
                'relevance': 0.85
            }
        ]

        # Add 3-5 random items from mock data
        items_to_add = random.sample(mock_data, k=random.randint(3, 5))
        
        for item in items_to_add:
            # Check if exists to avoid duplicates
            if not Bookmark.objects(user=user, url=item['url']).first():
                bookmark = Bookmark(
                    user=user,
                    title=item['title'],
                    url=item['url'],
                    description=item['desc'],
                    category=item['type'],  # Mapping type to category for now
                    tags=item['topic'],
                    relevance_score=item['relevance'],
                    # New fields would be set here if we extended the model
                    # For now we'll pack source into metadata or tags if needed
                    # but ideally we update the model first.
                    source=item['source'],
                    resource_type=item['type'],
                    topic=item['topic']
                )
                
                bookmark.save()
                new_resources.append(item['title'])

        return True, f"Synced {len(new_resources)} new resources from connected accounts."

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
            
        # Ensure directory exists
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'library')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_name = f"{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(upload_folder, save_name)
        file.save(file_path)
        
        # Create Bookmark entry
        bookmark = Bookmark(
            user=user,
            title=title or filename,
            url=f"/static/uploads/library/{save_name}", # Local URL
            description=f"Uploaded manual document: {filename}",
            category='document',
            tags=topic,
            relevance_score=1.0, # Manual uploads are highly relevant
            source='Manual Upload',
            resource_type='document',
            topic=topic,
            is_uploaded=True,
            file_path=file_path
        )
        
        bookmark.save()
        
        return True, "File uploaded successfully"
