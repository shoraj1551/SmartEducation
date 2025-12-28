"""
Calendar Routes for Phase 34.2: Google Calendar Integration
Handles OAuth flow and calendar sync operations
"""
from flask import Blueprint, request, jsonify, redirect, current_app
from app.routes.user_routes import token_required
from app.services.google_calendar_service import GoogleCalendarService
from app.models import User

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')


@calendar_bp.route('/google/auth', methods=['GET'])
@token_required
def google_auth(user_id):
    """Initiate Google Calendar OAuth flow"""
    try:
        auth_url = GoogleCalendarService.get_authorization_url(user_id)
        return jsonify({'authorization_url': auth_url}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to initiate OAuth: {str(e)}'}), 500


@calendar_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')  # This contains user_id
        
        if not code or not state:
            return jsonify({'error': 'Missing authorization code or state'}), 400
        
        user_id = state
        result = GoogleCalendarService.handle_oauth_callback(code, user_id)
        
        # Redirect to settings page with success message
        return redirect(f'/settings?calendar_connected=true')
        
    except ValueError as e:
        return redirect(f'/settings?calendar_error={str(e)}')
    except Exception as e:
        return redirect(f'/settings?calendar_error=Connection failed')


@calendar_bp.route('/google/status', methods=['GET'])
@token_required
def google_status(user_id):
    """Check Google Calendar connection status"""
    try:
        user = User.objects.get(id=user_id)
        return jsonify({
            'connected': user.google_calendar_connected,
            'token_expiry': user.google_calendar_token_expiry.isoformat() if user.google_calendar_token_expiry else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route('/google/disconnect', methods=['POST'])
@token_required
def google_disconnect(user_id):
    """Disconnect Google Calendar"""
    try:
        result = GoogleCalendarService.disconnect_calendar(user_id)
        return jsonify({'message': result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to disconnect: {str(e)}'}), 500


@calendar_bp.route('/google/sync', methods=['POST'])
@token_required
def manual_sync(user_id):
    """Manually trigger sync of all active commitments"""
    try:
        from app.models import Commitment
        from app.services.commitment_service import CommitmentService
        
        user = User.objects.get(id=user_id)
        
        if not user.google_calendar_connected:
            return jsonify({'error': 'Google Calendar not connected'}), 400
        
        # Get all active commitments
        commitments = Commitment.objects(user_id=user, status='active')
        
        synced_count = 0
        for commitment in commitments:
            # Only sync if not already synced
            if not commitment.commitment_metadata or 'google_calendar_event_id' not in commitment.commitment_metadata:
                try:
                    GoogleCalendarService.sync_commitment_to_google(commitment)
                    synced_count += 1
                except Exception as e:
                    print(f"Failed to sync commitment {commitment.id}: {e}")
        
        return jsonify({
            'message': f'Synced {synced_count} commitments to Google Calendar',
            'synced_count': synced_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Sync failed: {str(e)}'}), 500
