"""
Proof of Learning Routes for Feature 10: Proof-of-Learning System
API endpoints for quizzes, certificates, and portfolios
"""
from flask import Blueprint, request, jsonify
from app.services.proof_of_learning_service import ProofOfLearningService
from app.services.auth_service import AuthService
from functools import wraps

proof_bp = Blueprint('proof', __name__, url_prefix='/api/proof')


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


@proof_bp.route('/quiz/create', methods=['POST'])
@token_required
def create_quiz(user_id):
    """Create a quiz for a learning item"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        quiz = ProofOfLearningService.create_quiz(
            learning_item_id=data['learning_item_id'],
            quiz_data=data
        )
        
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz': quiz.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to create quiz: {str(e)}'}), 500


@proof_bp.route('/quiz/<quiz_id>/submit', methods=['POST'])
@token_required
def submit_quiz(user_id, quiz_id):
    """Submit quiz attempt"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({'error': 'answers are required'}), 400
        
        attempt = ProofOfLearningService.submit_quiz_attempt(
            quiz_id=quiz_id,
            user_id=user_id,
            answers=data['answers']
        )
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'attempt': attempt.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to submit quiz: {str(e)}'}), 500


@proof_bp.route('/certificate/issue', methods=['POST'])
@token_required
def issue_certificate(user_id):
    """Issue a certificate"""
    try:
        data = request.get_json()
        
        if not data or 'learning_item_id' not in data:
            return jsonify({'error': 'learning_item_id is required'}), 400
        
        certificate = ProofOfLearningService.issue_certificate(
            user_id=user_id,
            learning_item_id=data['learning_item_id'],
            certificate_type=data.get('certificate_type', 'completion')
        )
        
        return jsonify({
            'message': 'Certificate issued successfully',
            'certificate': certificate.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to issue certificate: {str(e)}'}), 500


@proof_bp.route('/certificates', methods=['GET'])
@token_required
def get_certificates(user_id):
    """Get user's certificates"""
    try:
        certificates = ProofOfLearningService.get_user_certificates(user_id)
        
        return jsonify({
            'certificates': [cert.to_dict() for cert in certificates],
            'count': len(certificates)
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get certificates: {str(e)}'}), 500


@proof_bp.route('/verify/<verification_code>', methods=['GET'])
def verify_certificate(verification_code):
    """Verify a certificate (public endpoint)"""
    try:
        result = ProofOfLearningService.verify_certificate(verification_code)
        
        return jsonify(result), 200 if result['valid'] else 404
    
    except Exception as e:
        return jsonify({'error': f'Failed to verify certificate: {str(e)}'}), 500


@proof_bp.route('/portfolio/<user_id>', methods=['GET'])
def get_portfolio(user_id):
    """Get public portfolio (public endpoint)"""
    try:
        portfolio = ProofOfLearningService.get_public_portfolio(user_id)
        
        return jsonify(portfolio), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get portfolio: {str(e)}'}), 500
