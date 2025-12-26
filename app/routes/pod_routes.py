"""
Pod Sharing API Routes
"""
from flask import Blueprint, request, jsonify
from app.services.pod_sharing_service import PodSharingService
from app.routes.user_routes import token_required

pod_bp = Blueprint('pod', __name__, url_prefix='/api/pod')


@pod_bp.route('/share', methods=['POST'])
@token_required
def share_content(current_user):
    """Share content with pod partners"""
    data = request.json
    
    try:
        result = PodSharingService.share_content(
            user_id=current_user.id,
            content_type=data['content_type'],
            content_id=data['content_id'],
            content_title=data.get('content_title', ''),
            partner_ids=data['partner_ids'],
            permissions=data.get('permissions')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@pod_bp.route('/share/<share_id>', methods=['DELETE'])
@token_required
def unshare_content(current_user, share_id):
    """Remove a share"""
    try:
        PodSharingService.unshare_content(current_user.id, share_id)
        return jsonify({'message': 'Content unshared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@pod_bp.route('/my-shares', methods=['GET'])
@token_required
def get_my_shares(current_user):
    """Get all content I've shared"""
    shares = PodSharingService.get_my_shared_content(current_user.id)
    return jsonify(shares), 200


@pod_bp.route('/shared-with-me', methods=['GET'])
@token_required
def get_shared_with_me(current_user):
    """Get all content shared with me"""
    shares = PodSharingService.get_shared_with_me(current_user.id)
    return jsonify(shares), 200


@pod_bp.route('/message', methods=['POST'])
@token_required
def send_message(current_user):
    """Send a message to a pod partner"""
    data = request.json
    
    try:
        result = PodSharingService.send_message(
            sender_id=current_user.id,
            receiver_id=data['receiver_id'],
            message_text=data['message']
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@pod_bp.route('/messages/<partner_id>', methods=['GET'])
@token_required
def get_messages(current_user, partner_id):
    """Get message thread with a partner"""
    try:
        messages = PodSharingService.get_messages(current_user.id, partner_id)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@pod_bp.route('/messages/unread-count', methods=['GET'])
@token_required
def get_unread_count(current_user):
    """Get count of unread messages"""
    count = PodSharingService.get_unread_count(current_user.id)
    return jsonify({'count': count}), 200
