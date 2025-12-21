"""
Inbox Routes for Unified Learning Inbox Feature
API endpoints for managing learning items
"""
from flask import Blueprint, request, jsonify
from app.services.inbox_service import InboxService
from app.services.auth_service import AuthService
from functools import wraps

inbox_bp = Blueprint('inbox', __name__, url_prefix='/api/inbox')


def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_id = AuthService.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Add user_id to kwargs
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated


@inbox_bp.route('/items', methods=['POST'])
@token_required
def create_item(user_id):
    """Create a new learning item"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        item = InboxService.create_learning_item(user_id, data)
        
        return jsonify({
            'message': 'Learning item created successfully',
            'item': item.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create item: {str(e)}'}), 500


@inbox_bp.route('/items', methods=['GET'])
@token_required
def get_items(user_id):
    """Get all learning items for the user with optional filtering"""
    try:
        # Get query parameters
        status_filter = request.args.get('status')  # active, paused, completed, dropped
        limit = request.args.get('limit', type=int)
        skip = request.args.get('skip', default=0, type=int)
        
        items = InboxService.get_user_items(
            user_id=user_id,
            status_filter=status_filter,
            limit=limit,
            skip=skip
        )
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'count': len(items)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch items: {str(e)}'}), 500


@inbox_bp.route('/items/<item_id>', methods=['GET'])
@token_required
def get_item(user_id, item_id):
    """Get a specific learning item"""
    try:
        item = InboxService.get_item_by_id(item_id, user_id)
        
        if not item:
            return jsonify({'error': 'Item not found or access denied'}), 404
        
        return jsonify({'item': item.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch item: {str(e)}'}), 500


@inbox_bp.route('/items/<item_id>/status', methods=['PUT'])
@token_required
def update_status(user_id, item_id):
    """Update the status of a learning item"""
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        new_status = data['status']
        item = InboxService.update_item_status(item_id, new_status, user_id)
        
        return jsonify({
            'message': f'Item status updated to {new_status}',
            'item': item.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to update status: {str(e)}'}), 500


@inbox_bp.route('/items/<item_id>/progress', methods=['PUT'])
@token_required
def update_progress(user_id, item_id):
    """Update the progress of a learning item"""
    try:
        data = request.get_json()
        
        if not data or 'completed_duration' not in data:
            return jsonify({'error': 'completed_duration is required'}), 400
        
        completed_duration = data['completed_duration']
        item = InboxService.update_progress(item_id, completed_duration, user_id)
        
        return jsonify({
            'message': 'Progress updated successfully',
            'item': item.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500


@inbox_bp.route('/items/<item_id>', methods=['DELETE'])
@token_required
def delete_item(user_id, item_id):
    """Delete a learning item"""
    try:
        InboxService.delete_item(item_id, user_id)
        
        return jsonify({'message': 'Item deleted successfully'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete item: {str(e)}'}), 500


@inbox_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(user_id):
    """Get inbox statistics for the user"""
    try:
        stats = InboxService.get_inbox_stats(user_id)
        
        return jsonify({'stats': stats}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500


@inbox_bp.route('/items/bulk-update', methods=['PUT'])
@token_required
def bulk_update(user_id):
    """Bulk update status for multiple items"""
    try:
        data = request.get_json()
        
        if not data or 'item_ids' not in data or 'status' not in data:
            return jsonify({'error': 'item_ids and status are required'}), 400
        
        item_ids = data['item_ids']
        new_status = data['status']
        
        result = InboxService.bulk_update_status(item_ids, new_status, user_id)
        
        return jsonify({
            'message': f'Bulk update completed',
            'updated_count': len(result['updated_items']),
            'updated_items': [item.to_dict() for item in result['updated_items']],
            'errors': result['errors']
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Bulk update failed: {str(e)}'}), 500


@inbox_bp.route('/check-capacity', methods=['GET'])
@token_required
def check_capacity(user_id):
    """Check if user can add new items and get detailed feedback"""
    try:
        result = InboxService.check_can_add_item(user_id)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to check capacity: {str(e)}'}), 500


@inbox_bp.route('/blocking-details', methods=['GET'])
@token_required
def get_blocking_details(user_id):
    """Get detailed information about why adding items is blocked"""
    try:
        details = InboxService.get_blocking_details(user_id)
        
        return jsonify(details), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get blocking details: {str(e)}'}), 500


@inbox_bp.route('/validate-addition', methods=['POST'])
@token_required
def validate_addition(user_id):
    """Validate if an item can be added before actually creating it"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        force = data.get('force', False)  # Admin override
        validation_result = InboxService.validate_item_addition(user_id, data, force)
        
        status_code = 200 if validation_result['can_proceed'] else 400
        
        return jsonify(validation_result), status_code
    
    except Exception as e:
        return jsonify({'error': f'Validation failed: {str(e)}'}), 500

