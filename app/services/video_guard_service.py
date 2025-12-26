
"""
VideoGuard Service (Feature 7)
Sanitizes video URLs to remove distraction algorithms (recommendations, related videos).
"""
import re

from app.constants import YOUTUBE_EMBED_URL_TEMPLATE, VIMEO_EMBED_URL_TEMPLATE

class VideoGuardService:
    
    @staticmethod
    def sanitize_url(url):
        """
        Convert a standard video URL into a distraction-free embed URL.
        Supported: YouTube, Vimeo (Basic).
        """
        if not url: return None
        
        # YOUTUBE MATCHING
        # Matches: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID
        yt_pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        yt_match = re.search(yt_pattern, url)
        
        if yt_match:
            video_id = yt_match.group(1)
            # Strict Mode Parameters:
            # rel=0: No related videos from other channels (only self, though YT changed this recently, it helps)
            # modestbranding=1: Remove big YT logo
            # controls=1: Allow control but minimal
            # iv_load_policy=3: Hide annotations
            return YOUTUBE_EMBED_URL_TEMPLATE.format(video_id=video_id)
            
        # VIMEO MATCHING
        vimeo_pattern = r'vimeo\.com\/(?:channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|video\/|)(\d+)'
        vimeo_match = re.search(vimeo_pattern, url)
        
        if vimeo_match:
            video_id = vimeo_match.group(1)
            return VIMEO_EMBED_URL_TEMPLATE.format(video_id=video_id) # do not track
            
        return url # Return original if no match (maybe text link)
