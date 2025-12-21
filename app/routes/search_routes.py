
"""
Search Routes (Feature 15)
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.search_service import SearchService
from functools import wraps

search_bp = Blueprint('search', __name__, url_prefix='/api')

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

@search_bp.route('/search', methods=['GET'])
@token_required
def search(user_id):
    query = request.args.get('q', '')
    try:
        results = SearchService.universal_search(user_id, query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
