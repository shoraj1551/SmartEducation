
"""
Search Service (Feature 15)
Universal Text Search across collections.
"""
from app.models import LearningItem, DailyTask, Flashcard
from mongoengine.queryset.visitor import Q

class SearchService:
    
    @staticmethod
    def universal_search(user_id, query):
        """
        Perform text search across multiple collections.
        Returns grouped results.
        """
        results = {
            'tasks': [],
            'library': [],
            'flashcards': []
        }
        
        if not query: return results
        
        # 1. Search Learning Items (Library)
        # Using search_text if index exists, else partial regex for MVP fallback resilience
        # Since we added indexes, search_text should work IF indexes are built.
        # MongoEngine builds indexes on app start usually.
        # Fallback: regex for safety during dev/hot-reload
        
        # LIBRARY
        items = LearningItem.objects.filter(
            Q(user_id=user_id) & (Q(title__icontains=query) | Q(description__icontains=query))
        ).limit(5)
        
        for item in items:
            results['library'].append({
                'id': str(item.id),
                'title': item.title,
                'subtitle': item.content_type.capitalize() if item.content_type else 'Resource',
                'link': '/bookmarks',  # Ideally deep link
                'icon': 'fa-book'
            })
            
        # TASKS
        tasks = DailyTask.objects.filter(
            Q(user_id=user_id) & Q(title__icontains=query)
        ).limit(5)
        
        for t in tasks:
            results['tasks'].append({
                'id': str(t.id),
                'title': t.title,
                'subtitle': f"{t.status} • {t.duration_minutes}m",
                'link': '/dashboard',
                'icon': 'fa-check-square'
            })
            
        # FLASHCARDS
        cards = Flashcard.objects.filter(
            Q(user_id=user_id) & (Q(front__icontains=query) | Q(back__icontains=query))
        ).limit(5)
        
        for c in cards:
            results['flashcards'].append({
                'id': str(c.id),
                'title': c.front,
                'subtitle': 'Flashcard',
                'link': '/flashcards',
                'icon': 'fa-clone'
            })
            
        return results
