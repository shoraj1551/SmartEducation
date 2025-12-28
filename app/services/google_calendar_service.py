"""
Google Calendar Service for Phase 34.2: Two-Way Calendar Sync
Handles OAuth authentication and syncing commitments with Google Calendar
"""
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app, url_for
from app.models import User, Commitment
from mongoengine.errors import DoesNotExist


class GoogleCalendarService:
    """Service for Google Calendar integration"""
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    
    @staticmethod
    def get_authorization_url(user_id):
        """
        Generate Google OAuth authorization URL
        
        Args:
            user_id: User ID to associate with the OAuth flow
            
        Returns:
            Authorization URL for user to visit
        """
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": current_app.config.get('GOOGLE_CLIENT_ID'),
                        "client_secret": current_app.config.get('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [current_app.config.get('GOOGLE_REDIRECT_URI')]
                    }
                },
                scopes=GoogleCalendarService.SCOPES
            )
            
            flow.redirect_uri = current_app.config.get('GOOGLE_REDIRECT_URI')
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=str(user_id)  # Pass user_id in state for callback
            )
            
            return authorization_url
            
        except Exception as e:
            print(f"Error generating auth URL: {e}")
            raise ValueError(f"Failed to generate authorization URL: {str(e)}")
    
    @staticmethod
    def handle_oauth_callback(code, user_id):
        """
        Handle OAuth callback and store tokens
        
        Args:
            code: Authorization code from Google
            user_id: User ID to associate tokens with
            
        Returns:
            Success message
        """
        try:
            user = User.objects.get(id=user_id)
            
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": current_app.config.get('GOOGLE_CLIENT_ID'),
                        "client_secret": current_app.config.get('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [current_app.config.get('GOOGLE_REDIRECT_URI')]
                    }
                },
                scopes=GoogleCalendarService.SCOPES
            )
            
            flow.redirect_uri = current_app.config.get('GOOGLE_REDIRECT_URI')
            flow.fetch_token(code=code)
            
            credentials = flow.credentials
            
            # Store tokens in user model
            user.google_calendar_token = credentials.token
            user.google_calendar_refresh_token = credentials.refresh_token
            user.google_calendar_token_expiry = credentials.expiry
            user.google_calendar_connected = True
            user.save()
            
            return "Google Calendar connected successfully!"
            
        except DoesNotExist:
            raise ValueError("User not found")
        except Exception as e:
            print(f"OAuth callback error: {e}")
            raise ValueError(f"Failed to connect Google Calendar: {str(e)}")
    
    @staticmethod
    def get_calendar_service(user):
        """
        Get authenticated Google Calendar service
        
        Args:
            user: User object with Google Calendar tokens
            
        Returns:
            Google Calendar API service object
        """
        if not user.google_calendar_connected:
            raise ValueError("Google Calendar not connected")
        
        credentials = Credentials(
            token=user.google_calendar_token,
            refresh_token=user.google_calendar_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=current_app.config.get('GOOGLE_CLIENT_ID'),
            client_secret=current_app.config.get('GOOGLE_CLIENT_SECRET'),
            scopes=GoogleCalendarService.SCOPES
        )
        
        # Refresh token if expired
        if credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
            
            # Update stored tokens
            user.google_calendar_token = credentials.token
            user.google_calendar_token_expiry = credentials.expiry
            user.save()
        
        return build('calendar', 'v3', credentials=credentials)
    
    @staticmethod
    def sync_commitment_to_google(commitment):
        """
        Sync a commitment to Google Calendar
        
        Args:
            commitment: Commitment object to sync
            
        Returns:
            Google Calendar event ID
        """
        try:
            user = commitment.user_id
            service = GoogleCalendarService.get_calendar_service(user)
            
            # Prepare event data
            event = {
                'summary': f'Study: {commitment.learning_item_id.title}',
                'description': f'Hard Commitment - {commitment.daily_study_minutes} minutes daily',
                'start': {
                    'dateTime': commitment.target_completion_date.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (commitment.target_completion_date + timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
                'recurrence': [
                    f'RRULE:FREQ=DAILY;COUNT={commitment.study_days_per_week * 4}'  # Approx 4 weeks
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            # Add time slot if specified
            if commitment.preferred_time_slot:
                # Parse time slot (e.g., "09:00-09:30")
                start_time, end_time = commitment.preferred_time_slot.split('-')
                event['start']['dateTime'] = f"{commitment.target_completion_date.date()}T{start_time}:00"
                event['end']['dateTime'] = f"{commitment.target_completion_date.date()}T{end_time}:00"
            
            # Create event
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            
            # Store event ID in commitment metadata
            if not commitment.commitment_metadata:
                commitment.commitment_metadata = {}
            commitment.commitment_metadata['google_calendar_event_id'] = created_event['id']
            commitment.save()
            
            return created_event['id']
            
        except HttpError as e:
            print(f"Google Calendar API error: {e}")
            raise ValueError(f"Failed to sync to Google Calendar: {str(e)}")
        except Exception as e:
            print(f"Sync error: {e}")
            raise ValueError(f"Failed to sync commitment: {str(e)}")
    
    @staticmethod
    def delete_google_event(commitment):
        """
        Delete a commitment event from Google Calendar
        
        Args:
            commitment: Commitment object with Google Calendar event
        """
        try:
            if not commitment.commitment_metadata or 'google_calendar_event_id' not in commitment.commitment_metadata:
                return  # No event to delete
            
            user = commitment.user_id
            service = GoogleCalendarService.get_calendar_service(user)
            
            event_id = commitment.commitment_metadata['google_calendar_event_id']
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            
        except HttpError as e:
            print(f"Failed to delete Google Calendar event: {e}")
        except Exception as e:
            print(f"Error deleting event: {e}")
    
    @staticmethod
    def disconnect_calendar(user_id):
        """
        Disconnect Google Calendar for a user
        
        Args:
            user_id: User ID to disconnect
        """
        try:
            user = User.objects.get(id=user_id)
            
            # Clear tokens
            user.google_calendar_token = None
            user.google_calendar_refresh_token = None
            user.google_calendar_token_expiry = None
            user.google_calendar_connected = False
            user.save()
            
            return "Google Calendar disconnected successfully"
            
        except DoesNotExist:
            raise ValueError("User not found")
