"""
Commitment Routes for Feature 3: Hard Commitment Mode
API endpoints for commitment management
"""
from flask import Blueprint, request, jsonify
from app.services.commitment_service import CommitmentService
from app.services.auth_service import AuthService
from functools import wraps
from datetime import datetime

commitments_bp = Blueprint('commitments', __name__, url_prefix='/api/commitments')


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


@commitments_bp.route('/', methods=['POST'])
@token_required
def create_commitment(user_id):
    """Create a new commitment"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        # Parse target date
        if 'target_completion_date' in data:
            data['target_completion_date'] = datetime.fromisoformat(data['target_completion_date'].replace('Z', '+00:00'))
        
        commitment = CommitmentService.create_commitment(
            user_id=user_id,
            learning_item_id=data['learning_item_id'],
            commitment_data=data
        )
        
        return jsonify({
            'message': 'Commitment created successfully',
            'commitment': commitment.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create commitment: {str(e)}'}), 500


@commitments_bp.route('/active', methods=['GET'])
@token_required
def get_active_commitments(user_id):
    """Get all active commitments"""
    try:
        commitments = CommitmentService.get_active_commitments(user_id)
        
        return jsonify({
            'commitments': [c.to_dict() for c in commitments],
            'count': len(commitments)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch commitments: {str(e)}'}), 500


@commitments_bp.route('/<commitment_id>/check-in', methods=['POST'])
@token_required
def check_in(user_id, commitment_id):
    """Daily check-in for a commitment"""
    try:
        data = request.get_json() or {}
        study_duration = data.get('study_duration_minutes', 0)
        
        commitment = CommitmentService.daily_check_in(commitment_id, study_duration)
        
        return jsonify({
            'message': 'Check-in successful',
            'commitment': commitment.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Check-in failed: {str(e)}'}), 500


@commitments_bp.route('/violations', methods=['GET'])
@token_required
def get_violations(user_id):
    """Get recent violations"""
    try:
        days = request.args.get('days', default=7, type=int)
        violations = CommitmentService.get_violations(user_id, days)
        
        return jsonify({
            'violations': [v.to_dict() for v in violations],
            'count': len(violations)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch violations: {str(e)}'}), 500


@commitments_bp.route('/lockout-status', methods=['GET'])
@token_required
def check_lockout_status(user_id):
    """Check if user is currently locked out"""
    try:
        is_locked_out = CommitmentService.is_user_locked_out(user_id)
        
        return jsonify({
            'is_locked_out': is_locked_out,
            'message': 'You are temporarily locked out from adding new content' if is_locked_out else 'No active lockouts'
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to check lockout status: {str(e)}'}), 500


@commitments_bp.route('/<commitment_id>/modify', methods=['PUT'])
@token_required
def modify_commitment(user_id, commitment_id):
    """Modify a commitment (limited modifications)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Parse target date if provided
        if 'target_completion_date' in data:
            data['target_completion_date'] = datetime.fromisoformat(data['target_completion_date'].replace('Z', '+00:00'))
        
        commitment = CommitmentService.modify_commitment(commitment_id, data)
        
        return jsonify({
            'message': 'Commitment modified successfully',
            'commitment': commitment.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to modify commitment: {str(e)}'}), 500
