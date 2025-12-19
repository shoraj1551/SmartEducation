"""
Bookmark API routes for SmartEducation
"""
from flask import Blueprint, request, jsonify
from routes.user_routes import token_required
from services.bookmark_service import BookmarkService
from models import Bookmark

bookmark_bp = Blueprint('bookmark', __name__, url_prefix='/api/bookmarks')

@bookmark_bp.route('', methods=['POST'])
@token_required
def add_bookmark(current_user):
    """Add a new bookmark"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
        
    bookmark, message = BookmarkService.add_bookmark(
        current_user.id,
        data['url'],
        data.get('title'),
        data.get('description'),
        data.get('tags')
    )
    
    if bookmark:
        return jsonify({
            'message': message,
            'bookmark': bookmark.to_dict()
        }), 201
    return jsonify({'error': message}), 500

@bookmark_bp.route('', methods=['GET'])
@token_required
def get_bookmarks(current_user):
    """Get paginated bookmarks for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    bookmarks, total = BookmarkService.get_bookmarks(current_user.email, page, per_page)
    
    return jsonify({
        'bookmarks': [b.to_dict() for b in bookmarks],
        'total': total,
        'page': page,
        'per_page': per_page
    }), 200

@bookmark_bp.route('/<string:bookmark_id>', methods=['DELETE'])
@token_required
def delete_bookmark(current_user, bookmark_id):
    """Delete a bookmark"""
    bookmark = Bookmark.objects(id=bookmark_id, user_id=current_user.id).first()
    if not bookmark:
        return jsonify({'error': 'Bookmark not found'}), 404
        
    bookmark.delete()
    return jsonify({'message': 'Bookmark deleted successfully'}), 200
