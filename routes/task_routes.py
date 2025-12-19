"""
Task Routes for Feature 2: Auto Course Breakdown
API endpoints for task generation and management
"""
from flask import Blueprint, request, jsonify
from services.task_generator_service import TaskGeneratorService
from services.auth_service import AuthService
from functools import wraps
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_data = AuthService.verify_token(token)
            if not user_data:
                return jsonify({'error': 'Invalid token'}), 401
            
            kwargs['user_id'] = user_data['user_id']
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated


@tasks_bp.route('/generate', methods=['POST'])
@token_required
def generate_plan(user_id):
    """Generate a learning plan with daily tasks for a learning item"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        # Parse target date
        if 'target_completion_date' in data:
            data['target_completion_date'] = datetime.fromisoformat(data['target_completion_date'].replace('Z', '+00:00'))
        
        plan = TaskGeneratorService.generate_learning_plan(
            learning_item_id=data['learning_item_id'],
            user_id=user_id,
            plan_config=data
        )
        
        return jsonify({
            'message': 'Learning plan generated successfully',
            'plan': plan.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to generate plan: {str(e)}'}), 500


@tasks_bp.route('/today', methods=['GET'])
@token_required
def get_today_tasks(user_id):
    """Get all tasks scheduled for today"""
    try:
        tasks = TaskGeneratorService.get_today_tasks(user_id)
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch today\'s tasks: {str(e)}'}), 500


@tasks_bp.route('/<task_id>/complete', methods=['PUT'])
@token_required
def complete_task(user_id, task_id):
    """Mark a task as completed"""
    try:
        data = request.get_json() or {}
        actual_duration = data.get('actual_duration_minutes')
        
        task = TaskGeneratorService.complete_task(task_id, actual_duration)
        
        return jsonify({
            'message': 'Task completed successfully',
            'task': task.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to complete task: {str(e)}'}), 500


@tasks_bp.route('/reschedule', methods=['POST'])
@token_required
def reschedule_plan(user_id):
    """Reschedule a learning plan (adaptive rescheduling)"""
    try:
        data = request.get_json()
        
        if not data or 'plan_id' not in data:
            return jsonify({'error': 'plan_id is required'}), 400
        
        # Parse new target date if provided
        new_target_date = None
        if 'new_target_date' in data:
            new_target_date = datetime.fromisoformat(data['new_target_date'].replace('Z', '+00:00'))
        
        plan = TaskGeneratorService.reschedule_plan(
            plan_id=data['plan_id'],
            new_target_date=new_target_date,
            new_daily_minutes=data.get('new_daily_minutes')
        )
        
        return jsonify({
            'message': 'Plan rescheduled successfully',
            'plan': plan.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to reschedule plan: {str(e)}'}), 500
