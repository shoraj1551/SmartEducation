
"""
Commitment Routes for Hard Commitment Mode (Feature 3)
API endpoints for managing commitments, check-ins, and violations
"""
from flask import Blueprint, request, jsonify
from app.services.commitment_service import CommitmentService
from app.services.auth_service import AuthService
from functools import wraps

commitment_bp = Blueprint('commitment', __name__, url_prefix='/api/commitment')

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
            
            user_id = AuthService.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
            
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    return decorated

@commitment_bp.route('/create', methods=['POST'])
@token_required
def create_commitment(user_id):
    """Create a locked commitment for a learning item"""
    try:
        data = request.get_json()
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        learning_item_id = data['learning_item_id']
        commitment = CommitmentService.create_commitment(user_id, learning_item_id, data)
        
        return jsonify({
            'message': 'Commitment locked successfully',
            'commitment': commitment.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create commitment: {str(e)}'}), 500

@commitment_bp.route('/list', methods=['GET'])
@token_required
def list_commitments(user_id):
    """List active commitments"""
    try:
        commitments = CommitmentService.get_active_commitments(user_id)
        return jsonify({'commitments': [c.to_dict() for c in commitments]}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch commitments: {str(e)}'}), 500

@commitment_bp.route('/check-in', methods=['POST'])
@token_required
def daily_check_in(user_id):
    """Perform daily check-in"""
    try:
        data = request.get_json()
        if not data or 'commitment_id' not in data or 'study_duration' not in data:
            return jsonify({'error': 'commitment_id and study_duration are required'}), 400
        
        commitment = CommitmentService.daily_check_in(
            data['commitment_id'], 
            data['study_duration']
        )
        
        return jsonify({
            'message': 'Check-in successful',
            'commitment': commitment.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Check-in failed: {str(e)}'}), 500

@commitment_bp.route('/modify/<commitment_id>', methods=['PUT'])
@token_required
def modify_commitment(user_id, commitment_id):
    """Modify a commitment (limited attempts)"""
    try:
        data = request.get_json()
        commitment = CommitmentService.modify_commitment(commitment_id, data)
        return jsonify({
            'message': 'Commitment modified successfully',
            'commitment': commitment.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Modification failed: {str(e)}'}), 500

@commitment_bp.route('/violations', methods=['GET'])
@token_required
def get_violations(user_id):
    """Get recent violations"""
    try:
        violations = CommitmentService.get_violations(user_id)
        return jsonify({'violations': [v.to_dict() for v in violations]}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch violations: {str(e)}'}), 500


@commitment_bp.route('/validate', methods=['POST'])
@token_required
def validate_plan(user_id):
    """
    Validate a proposed study plan (Reality Check)
    """
    try:
        data = request.get_json()
        if not data: 
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['learning_item_id', 'target_completion_date', 'daily_study_minutes']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
                
        learning_item_id = data['learning_item_id']
        target_date_str = data['target_completion_date']
        daily_minutes = data['daily_study_minutes']
        study_days = data.get('study_days_per_week', 5)
        
        # Parse Date
        from datetime import datetime
        try:
            target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00'))
        except ValueError:
             return jsonify({'error': 'Invalid date format. Use ISO 8601'}), 400

        from app.services.reality_service import RealityService
        result = RealityService.check_feasibility(
            user_id, learning_item_id, target_date, daily_minutes, study_days
        )
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': f'Validation failed: {str(e)}'}), 500
