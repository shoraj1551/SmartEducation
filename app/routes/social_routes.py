
"""
Social Routes (Feature 13)
API for Pods and Accountability.
"""
from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from app.services.accountability_service import AccountabilityService
from app.models import AccountabilityPartner
from functools import wraps

social_bp = Blueprint('social', __name__, url_prefix='/api/social')

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

@social_bp.route('/invite', methods=['POST'])
@token_required
def send_invite(user_id):
    try:
        data = request.get_json()
        email = data.get('email')
        msg = AccountabilityService.send_invite(user_id, email)
        return jsonify({'message': msg}), 200
    except ValueError as e: return jsonify({'error': str(e)}), 400
    except Exception as e: return jsonify({'error': str(e)}), 500

@social_bp.route('/invites', methods=['GET'])
@token_required
def get_invites(user_id):
    """Get pending invites sent TO me"""
    try:
        # User needs to check both invites they sent AND received?
        # Received: AccountabilityPartner where partner_email == my_email and status='pending'
        from app.models import User
        me = User.objects.get(id=user_id)
        
        invites = AccountabilityPartner.objects(
            partner_email=me.email,
            status='pending'
        )
        
        data = []
        for i in invites:
            sender = i.user_id
            data.append({
                'id': str(i.id),
                'sender_name': sender.name,
                'sender_email': sender.email,
                'sent_at': i.invited_at.isoformat()
            })
        return jsonify(data), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@social_bp.route('/invites/<invite_id>/accept', methods=['POST'])
@token_required
def accept_invite(user_id, invite_id):
    try:
        msg = AccountabilityService.accept_invite(invite_id, user_id)
        return jsonify({'message': msg}), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@social_bp.route('/pod', methods=['GET'])
@token_required
def get_pod(user_id):
    try:
        pod = AccountabilityService.get_pod(user_id)
        return jsonify(pod), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@social_bp.route('/nudge', methods=['POST'])
@token_required
def nudge(user_id):
    try:
        data = request.get_json()
        partner_id = data.get('partner_id')
        AccountabilityService.nudge_partner(user_id, partner_id)
        return jsonify({'message': 'Nudge sent'}), 200
    except Exception as e: return jsonify({'error': str(e)}), 500
