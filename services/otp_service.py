"""
OTP Service for email and SMS verification
"""
import random
import string
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Mail, Message
from twilio.rest import Client
from models import db, OTP

mail = Mail()

class OTPService:
    """Service for OTP generation and delivery"""
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_otp(user_id, otp_type, purpose):
        """Create and store OTP in database"""
        # Delete any existing OTPs for this user, type, and purpose
        OTP.query.filter_by(
            user_id=user_id,
            otp_type=otp_type,
            purpose=purpose,
            is_used=False
        ).delete()
        
        # Generate new OTP
        otp_code = OTPService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(
            minutes=current_app.config['OTP_EXPIRY_MINUTES']
        )
        
        # Create OTP record
        otp = OTP(
            user_id=user_id,
            otp_code=otp_code,
            otp_type=otp_type,
            purpose=purpose,
            expires_at=expires_at
        )
        
        db.session.add(otp)
        db.session.commit()
        
        return otp
    
    @staticmethod
    def send_email_otp(email, otp_code, purpose):
        """Send OTP via email using Mailtrap"""
        try:
            subject = f"SmartEducation - Your OTP for {purpose.title()}"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                        <h2 style="color: #667eea;">SmartEducation</h2>
                        <h3>Your OTP Code</h3>
                        <p>Your OTP for {purpose} is:</p>
                        <div style="background-color: #f0f0f0; padding: 20px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 5px; border-radius: 5px; margin: 20px 0;">
                            {otp_code}
                        </div>
                        <p style="color: #666;">This OTP will expire in {current_app.config['OTP_EXPIRY_MINUTES']} minutes.</p>
                        <p style="color: #666;">If you didn't request this OTP, please ignore this email.</p>
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #999; font-size: 12px;">© 2025 SmartEducation. All rights reserved.</p>
                    </div>
                </body>
            </html>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=body
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error sending email OTP: {str(e)}")
            return False
    
    @staticmethod
    def send_sms_otp(mobile, otp_code, purpose):
        """Send OTP via SMS using Twilio"""
        try:
            client = Client(
                current_app.config['TWILIO_ACCOUNT_SID'],
                current_app.config['TWILIO_AUTH_TOKEN']
            )
            
            message = client.messages.create(
                body=f"Your SmartEducation OTP for {purpose} is: {otp_code}. Valid for {current_app.config['OTP_EXPIRY_MINUTES']} minutes.",
                from_=current_app.config['TWILIO_PHONE_NUMBER'],
                to=mobile
            )
            
            return True
            
        except Exception as e:
            print(f"Error sending SMS OTP: {str(e)}")
            return False
    
    @staticmethod
    def verify_otp(user_id, otp_code, otp_type, purpose):
        """Verify OTP code"""
        otp = OTP.query.filter_by(
            user_id=user_id,
            otp_type=otp_type,
            purpose=purpose,
            is_used=False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            return False, "OTP not found"
        
        if otp.is_expired():
            return False, "OTP has expired"
        
        if otp.attempts >= current_app.config['OTP_MAX_ATTEMPTS']:
            return False, "Maximum attempts exceeded"
        
        # Increment attempts
        otp.attempts += 1
        
        if otp.otp_code != otp_code:
            db.session.commit()
            return False, f"Invalid OTP. {current_app.config['OTP_MAX_ATTEMPTS'] - otp.attempts} attempts remaining"
        
        # Mark as used
        otp.is_used = True
        db.session.commit()
        
        return True, "OTP verified successfully"
    
    @staticmethod
    def delete_user_otps(user_id):
        """Delete all OTP records for a user (used after registration completion)"""
        try:
            OTP.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting OTPs: {str(e)}")
            return False
