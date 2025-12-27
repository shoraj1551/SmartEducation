"""
Learning Plan routes for Auto Course Breakdown (Feature 2)
"""
from flask import Blueprint, request, jsonify
from app.models import LearningPlan, LearningItem, DailyTask
from app.services.auth_service import AuthService
from app.routes.user_routes import token_required
from datetime import datetime
import math

learning_bp = Blueprint('learning', __name__, url_prefix='/api/learning')

@learning_bp.route('/plans', methods=['POST'])
@token_required
def create_learning_plan(current_user):
    """Create a new automatic learning plan for an item"""
    data = request.get_json()
    
    if not data or 'learning_item_id' not in data or 'target_date' not in data:
        return jsonify({'error': 'Missing required fields: learning_item_id, target_date'}), 400
        
    try:
        item = LearningItem.objects(id=data['learning_item_id'], user_id=current_user.id).first()
        if not item:
            return jsonify({'error': 'Learning item not found'}), 404
            
        # Parse dates
        target_date = datetime.fromisoformat(data['target_date'].replace('Z', '+00:00'))
        
        # Calculate availability and duration
        # Simple default logic for now - typically this would come from the frontend wizard
        daily_minutes = data.get('daily_availability_minutes', 60)
        total_minutes = data.get('total_estimated_duration', item.total_duration)
        
        if total_minutes <= 0:
             return jsonify({'error': 'Total duration must be greater than 0'}), 400
             
        plan = LearningPlan(
            learning_item_id=item,
            user_id=current_user,
            target_completion_date=target_date,
            daily_availability_minutes=daily_minutes,
            total_estimated_duration=total_minutes,
            skip_weekends=data.get('skip_weekends', True),
            buffer_percentage=data.get('buffer_percentage', 20.0),
            status='active'
        )
        plan.save()
        
        # Trigger basic breakdown generation (simplistic V1)
        # In a real scenario, this would be a separate Service call (AutoBreakdownService)
        # For now, we stub the creation of tasks to prove the endpoint works
        
        return jsonify({
            'message': 'Learning Plan created successfully',
            'plan': plan.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/plans/<plan_id>', methods=['GET'])
@token_required
def get_learning_plan(current_user, plan_id):
    """Get a specific learning plan"""
    try:
        plan = LearningPlan.objects(id=plan_id, user_id=current_user.id).first()
        if not plan:
            return jsonify({'error': 'Learning Plan not found'}), 404
            
        return jsonify(plan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/plans/item/<item_id>', methods=['GET'])
@token_required
def get_plan_by_item(current_user, item_id):
    """Get learning plan for a specific item"""
    try:
        # Check item ownership first
        item = LearningItem.objects(id=item_id, user_id=current_user.id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
            
        plan = LearningPlan.objects(learning_item_id=item_id, user_id=current_user.id).first()
        if not plan:
            return jsonify({'message': 'No plan found for this item'}), 404
            
        return jsonify(plan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@learning_bp.route('/plans/<plan_id>/tasks', methods=['GET'])
@token_required
def get_plan_tasks(current_user, plan_id):
    """Get all daily tasks for a plan"""
    try:
        tasks = DailyTask.objects(learning_plan_id=plan_id, user_id=current_user.id).order_by('scheduled_date')
        return jsonify([t.to_dict() for t in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
