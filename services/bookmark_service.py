"""
Bookmark service for managing and filtering educational resources
"""
import re
import json
from models import db, Bookmark, User
from datetime import datetime

class BookmarkService:
    """Service for bookmark management and AI-driven filtering"""

    @staticmethod
    def classify_url(url, title, description):
        """
        AI-driven classification algorithm (Mocking GPT-like logic with robust heuristics)
        In a production environment, this would call an LLM API.
        """
        educational_keywords = [
            'tutorial', 'course', 'learn', 'education', 'lecture', 'guide', 'how-to',
            'documentation', 'wiki', 'study', 'class', 'university', 'bootcamp',
            'programming', 'science', 'math', 'history', 'language'
        ]
        
        # Educational domains/patterns
        edu_patterns = [
            r'youtube\.com/watch\?v=', r'coursera\.org', r'udemy\.com', 
            r'khanacademy\.org', r'github\.com', r'medium\.com', 
            r'stackoverflow\.com', r'edx\.org', r'wikipedia\.org'
        ]

        text_to_scan = f"{url} {title} {description}".lower()
        
        is_edu = any(re.search(pattern, url) for pattern in edu_patterns) or \
                 any(kw in text_to_scan for kw in educational_keywords)
        
        category = 'other'
        if 'youtube.com' in url or 'youtu.be' in url:
            category = 'video'
        elif any(d in url for d in ['docs.', 'wiki.', 'github.com']):
            category = 'article/docs'
        elif any(d in url for d in ['coursera', 'udemy', 'edx']):
            category = 'course'
            
        return is_edu, category

    @staticmethod
    def calculate_relevance(bookmark, user_goals):
        """
        Rank bookmark based on user learning goals.
        goals example: ['upskill', 'tech']
        """
        score = 0.0
        if not user_goals:
            return 0.5 # Default middle score
            
        text_to_scan = f"{bookmark.title} {bookmark.description} {bookmark.tags}".lower()
        
        for goal in user_goals:
            if goal.lower() in text_to_scan:
                score += 0.25
        
        # Boost if is_educational
        if bookmark.is_educational:
            score += 0.3
            
        return min(score, 1.0) # Cap at 1.0

    @staticmethod
    def add_bookmark(user_id, url, title=None, description=None, tags=None):
        """Add a new bookmark with AI metadata generation"""
        try:
            # 1. Classify
            is_edu, category = BookmarkService.classify_url(url, title or '', description or '')
            
            # 2. Extract Title if missing (In real app, fetch URL info)
            if not title:
                title = url.split('/')[-1] or "New Bookmark"

            bookmark = Bookmark(
                user_id=user_id,
                url=url,
                title=title,
                description=description,
                is_educational=is_edu,
                category=category,
                tags=tags
            )
            
            # 3. Calculate initial relevance if goals exist
            user = User.query.get(user_id)
            # Assuming user preferences are stored in a way we can access
            # For now, we'll leave it at default and update later
            
            db.session.add(bookmark)
            db.session.commit()
            return bookmark, "Bookmark added successfully"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_bookmarks(user_email, page=1, per_page=20):
        """Fetch paginated bookmarks for a user by email"""
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return [], 0
            
        pagination = Bookmark.query.filter_by(user_id=user.id)\
            .order_by(Bookmark.relevance_score.desc(), Bookmark.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
            
        return pagination.items, pagination.total
