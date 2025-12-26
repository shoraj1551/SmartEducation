"""
Advanced Pod Routes - Group Sharing, Activity Feed, Shared Goals
"""
from flask import Blueprint, request, jsonify
from app.services.advanced_pod_features import AdvancedPodFeatures
from app.routes.user_routes import token_required

advanced_pod_bp = Blueprint('advanced_pod', __name__, url_prefix='/api/pod/advanced')


@advanced_pod_bp.route('/share-with-group', methods=['POST'])
@token_required
def share_with_group(current_user):
    """Share content with entire pod at once"""
    data = request.json
    
    try:
        result = AdvancedPodFeatures.share_with_group(
            user_id=current_user.id,
            content_type=data['content_type'],
            content_id=data['content_id'],
            content_title=data.get('content_title', ''),
            group_name=data.get('group_name')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@advanced_pod_bp.route('/activity-feed', methods=['GET'])
@token_required
def get_activity_feed(current_user):
    """Get activity feed from pod partners"""
    limit = request.args.get('limit', 20, type=int)
    
    try:
        activities = AdvancedPodFeatures.get_activity_feed(current_user.id, limit)
        return jsonify(activities), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@advanced_pod_bp.route('/shared-goal', methods=['POST'])
@token_required
def create_shared_goal(current_user):
    """Create a shared goal with pod partners"""
    data = request.json
    
    try:
        result = AdvancedPodFeatures.create_shared_goal(
            user_id=current_user.id,
            goal_title=data['goal_title'],
            goal_description=data.get('goal_description', ''),
            target_date=data['target_date'],
            partner_ids=data['partner_ids']
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@advanced_pod_bp.route('/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(current_user):
    """Get pod leaderboard"""
    try:
        leaderboard = AdvancedPodFeatures.get_pod_leaderboard(current_user.id)
        return jsonify(leaderboard), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
