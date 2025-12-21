
"""
Recall Routes (Feature 12)
API for Flashcards and Spaced Repetition.
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.recall_service import RecallService
from app.models import Flashcard, LearningItem
from functools import wraps

recall_bp = Blueprint('recall', __name__, url_prefix='/api/recall')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token: return jsonify({'error': 'Token missing'}), 401
        try:
            if token.startswith('Bearer '): token = token[7:]
            user_id = AuthService.verify_token(token)
            if not user_id: return jsonify({'error': 'Invalid token'}), 401
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except: return jsonify({'error': 'Token error'}), 401
    return decorated

@recall_bp.route('/due', methods=['GET'])
@token_required
def get_due_cards(user_id):
    """Get cards due for review"""
    try:
        cards = RecallService.get_due_cards(user_id)
        return jsonify([c.to_dict() for c in cards]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recall_bp.route('/review', methods=['POST'])
@token_required
def submit_review(user_id):
    """Submit a review result"""
    try:
        data = request.get_json()
        card_id = data.get('card_id')
        quality = data.get('quality') # 0-5
        
        result = RecallService.process_review(card_id, int(quality))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recall_bp.route('/generate', methods=['POST'])
@token_required
def generate_cards(user_id):
    """Generate cards from text"""
    try:
        data = request.get_json()
        item_id = data.get('learning_item_id')
        text = data.get('text')
        
        count = RecallService.generate_cards_from_text(user_id, item_id, text)
        return jsonify({'message': f'{count} cards generated', 'count': count}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recall_bp.route('/create', methods=['POST'])
@token_required
def create_card(user_id):
    """Manually create a card"""
    try:
        data = request.get_json()
        item_id = data.get('learning_item_id')
        front = data.get('front')
        back = data.get('back')
        
        card = Flashcard(
            user_id=user_id,
            learning_item_id=item_id,
            front=front,
            back=back
        )
        card.save()
        return jsonify(card.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
