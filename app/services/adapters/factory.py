
from typing import Optional
from .base import BaseAdapter
from .youtube import YouTubeAdapter

class AdapterFactory:
    """
    Factory to get the correct adapter for a given URL or Source Type
    """
    
    _adapters = [
        YouTubeAdapter()
    ]
    
    @staticmethod
    def get_adapter(url: str) -> Optional[BaseAdapter]:
        """Auto-detect adapter from URL"""
        for adapter in AdapterFactory._adapters:
            if adapter.validate_url(url):
                return adapter
        return None
        
    @staticmethod
    def get_adapter_by_type(source_type: str) -> Optional[BaseAdapter]:
        """Get adapter by explicit type name"""
        for adapter in AdapterFactory._adapters:
            if adapter.platform_name == source_type:
                return adapter
        return None
