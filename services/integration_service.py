"""
Integration Service for External Platforms
Handles connections to YouTube, cloud storage, and other platforms
"""
from datetime import datetime
from models import ContentSource, User
from mongoengine.errors import DoesNotExist


class IntegrationService:
    """Service for managing external platform integrations"""
    
    @staticmethod
    def connect_platform(user_id, platform_data):
        """
        Connect a new platform for content import
        
        Args:
            user_id: User ID
            platform_data: Dictionary with platform details
            
        Returns:
            ContentSource object
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Check if platform already connected
        existing = ContentSource.objects(
            user_id=user,
            platform_name=platform_data['platform_name']
        ).first()
        
        if existing:
            raise ValueError(f"Platform {platform_data['platform_name']} already connected")
        
        source = ContentSource(
            user_id=user,
            platform_name=platform_data['platform_name'],
            platform_type=platform_data['platform_type'],
            is_connected=True,
            auto_sync=platform_data.get('auto_sync', False),
            sync_frequency=platform_data.get('sync_frequency', 'manual'),
            connection_metadata=platform_data.get('metadata', {})
        )
        
        source.save()
        return source
    
    @staticmethod
    def get_user_integrations(user_id):
        """Get all platform integrations for a user"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            return []
        
        return list(ContentSource.objects(user_id=user))
    
    @staticmethod
    def disconnect_platform(source_id, user_id):
        """Disconnect a platform integration"""
        try:
            source = ContentSource.objects.get(id=source_id)
            
            # Verify ownership
            if str(source.user_id.id) != str(user_id):
                raise ValueError("Access denied")
            
            source.delete()
            return True
        except DoesNotExist:
            raise ValueError("Integration not found")


class YouTubeIntegration:
    """YouTube API integration for playlist and video import"""
    
    @staticmethod
    def extract_video_id(url):
        """Extract video ID from YouTube URL"""
        # Basic implementation - can be enhanced with regex
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/watch?v=' in url:
            return url.split('v=')[1].split('&')[0]
        return None
    
    @staticmethod
    def extract_playlist_id(url):
        """Extract playlist ID from YouTube URL"""
        if 'list=' in url:
            return url.split('list=')[1].split('&')[0]
        return None
    
    @staticmethod
    def get_video_metadata(video_id):
        """
        Get video metadata from YouTube
        Note: Requires YouTube Data API key - placeholder implementation
        """
        # Placeholder - would use YouTube Data API v3
        return {
            'title': f'Video {video_id}',
            'duration': 600,  # in seconds
            'description': 'Video description',
            'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
        }
    
    @staticmethod
    def get_playlist_videos(playlist_id):
        """
        Get all videos from a YouTube playlist
        Note: Requires YouTube Data API key - placeholder implementation
        """
        # Placeholder - would use YouTube Data API v3
        return []


class PDFParser:
    """PDF parsing for local file import"""
    
    @staticmethod
    def extract_metadata(file_path):
        """
        Extract metadata from PDF file
        Note: Requires PyPDF2 or similar library
        """
        # Placeholder implementation
        return {
            'title': 'PDF Document',
            'pages': 0,
            'author': 'Unknown',
            'size_bytes': 0
        }
    
    @staticmethod
    def estimate_reading_time(page_count):
        """Estimate reading time based on page count (2 min per page average)"""
        return page_count * 2


class CloudStorageIntegration:
    """Integration with cloud storage providers (Google Drive, Dropbox)"""
    
    @staticmethod
    def connect_google_drive(user_id, access_token):
        """
        Connect Google Drive account
        Note: Requires Google Drive API setup
        """
        # Placeholder implementation
        return {
            'platform_name': 'google_drive',
            'platform_type': 'storage',
            'is_connected': True
        }
    
    @staticmethod
    def connect_dropbox(user_id, access_token):
        """
        Connect Dropbox account
        Note: Requires Dropbox API setup
        """
        # Placeholder implementation
        return {
            'platform_name': 'dropbox',
            'platform_type': 'storage',
            'is_connected': True
        }
    
    @staticmethod
    def list_files(source_id, folder_path='/'):
        """List files from connected cloud storage"""
        # Placeholder implementation
        return []


class CoursePlatformScraper:
    """Scraper for course platforms (Udemy, Coursera, etc.)"""
    
    @staticmethod
    def extract_course_info(url):
        """
        Extract course information from URL
        Note: Web scraping - should respect robots.txt and terms of service
        """
        # Placeholder implementation
        platform = None
        if 'udemy.com' in url:
            platform = 'udemy'
        elif 'coursera.org' in url:
            platform = 'coursera'
        elif 'edx.org' in url:
            platform = 'edx'
        
        return {
            'platform': platform,
            'title': 'Course Title',
            'duration': 0,
            'description': 'Course description'
        }
