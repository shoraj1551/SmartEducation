
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAdapter(ABC):
    """
    Abstract Base Class for Content Source Adapters.
    Standardizes how we fetch metadata and validate content from different platforms.
    """
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Name of the platform (e.g., 'youtube', 'coursera')"""
        pass
        
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Check if the URL belongs to this platform"""
        pass
        
    @abstractmethod
    def extract_id(self, url: str) -> Optional[str]:
        """Extract the unique content ID from the URL"""
        pass
        
    @abstractmethod
    def fetch_metadata(self, url: str) -> Dict[str, Any]:
        """
        Fetch rich metadata for the content.
        
        Returns:
            Dict containing:
            - title
            - description
            - duration_minutes (int)
            - thumbnail_url
            - author
            - published_at
            - platform_metadata (raw dict)
        """
        pass
