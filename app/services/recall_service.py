
"""
Recall Service (Feature 12)
Manages Active Recall and Spaced Repetition (SRS) logic.
"""
from app.models import Flashcard, LearningItem
from datetime import datetime, timedelta

class RecallService:
    
    @staticmethod
    def process_review(card_id, quality):
        """
        Process a review using SuperMemo-2 Algorithm.
        quality: 0 (blackout) to 5 (perfect response).
        """
        card = Flashcard.objects.get(id=card_id)
        
        # SM-2 Algorithm
        if quality < 3:
            # Failed recall
            card.repetitions = 0
            card.interval = 1
        else:
            # Successful recall
            card.repetitions += 1
            if card.repetitions == 1:
                card.interval = 1
            elif card.repetitions == 2:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.easiness_factor)
            
            # Update EF
            # EF' = EF + (0.1 - (5-q) * (0.08 + (5-q)*0.02))
            # q = quality
            q = quality
            new_ef = card.easiness_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
            if new_ef < 1.3:
                new_ef = 1.3
            card.easiness_factor = new_ef
            
        # Update dates
        card.last_reviewed_at = datetime.utcnow()
        card.next_review_date = datetime.utcnow() + timedelta(days=card.interval)
        card.save()
        
        return {
            'next_review': card.next_review_date.isoformat(),
            'interval': card.interval,
            'message': 'Scheduled for review in ' + str(card.interval) + ' days.'
        }

    @staticmethod
    def generate_cards_from_text(user_id, item_id, text):
        """
        Simple MVP generator: Splits text by double newlines.
        First line is Front, Rest is Back.
        """
        chunks = text.split('\n\n')
        cards_created = 0
        
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk: continue
            
            lines = chunk.split('\n')
            if len(lines) < 2: continue # Need at least Front and Back
            
            front = lines[0].strip()
            back = "\n".join(lines[1:]).strip()
            
            if len(front) > 5 and len(back) > 5:
                Flashcard(
                    user_id=user_id,
                    learning_item_id=item_id,
                    front=front,
                    back=back
                ).save()
                cards_created += 1
                
        return cards_created

    @staticmethod
    def get_due_cards(user_id):
        """Get cards due before or on today"""
        now = datetime.utcnow()
        return Flashcard.objects(
            user_id=user_id,
            next_review_date__lte=now
        ).order_by('next_review_date')
