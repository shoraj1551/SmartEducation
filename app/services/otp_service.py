"""
OTP Service for email and SMS verification
"""
import random
import string
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Mail, Message
from twilio.rest import Client
from app.models import OTP

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
        OTP.objects(
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
        
        otp.save()
        
        return otp
    
    @staticmethod
    def send_email_otp(email, otp_code, purpose):
        """Send OTP via email using Mailtrap"""
        try:
            # Check if SMTP credentials are configured
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                print(f"\n{'='*60}")
                print(f"⚠️  EMAIL CREDENTIALS NOT CONFIGURED")
                print(f"{'='*60}")
                print(f"📧 Email: {email}")
                print(f"🔐 OTP Code: {otp_code}")
                print(f"📝 Purpose: {purpose}")
                print(f"⏰ Expires in: {current_app.config['OTP_EXPIRY_MINUTES']} minutes")
                print(f"{'='*60}\n")
                return True  # Return True to allow testing without email
            
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
            print(f"✅ Email OTP sent successfully to {email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email OTP: {str(e)}")
            # Log the OTP for testing purposes
            print(f"📧 Email: {email} | 🔐 OTP: {otp_code} | 📝 Purpose: {purpose}")
            return True  # Return True to allow testing to continue
    
    @staticmethod
    def send_sms_otp(mobile, otp_code, purpose):
        """Send OTP via SMS using Twilio"""
        try:
            # Check if Twilio credentials are configured
            if not current_app.config.get('TWILIO_ACCOUNT_SID') or not current_app.config.get('TWILIO_AUTH_TOKEN'):
                print(f"\n{'='*60}")
                print(f"⚠️  TWILIO CREDENTIALS NOT CONFIGURED")
                print(f"{'='*60}")
                print(f"📱 Mobile: {mobile}")
                print(f"🔐 OTP Code: {otp_code}")
                print(f"📝 Purpose: {purpose}")
                print(f"⏰ Expires in: {current_app.config['OTP_EXPIRY_MINUTES']} minutes")
                print(f"{'='*60}\n")
                return True  # Return True to allow testing without SMS
            
            client = Client(
                current_app.config['TWILIO_ACCOUNT_SID'],
                current_app.config['TWILIO_AUTH_TOKEN']
            )
            
            message = client.messages.create(
                body=f"Your SmartEducation OTP for {purpose} is: {otp_code}. Valid for {current_app.config['OTP_EXPIRY_MINUTES']} minutes.",
                from_=current_app.config['TWILIO_PHONE_NUMBER'],
                to=mobile
            )
            
            print(f"✅ SMS OTP sent successfully to {mobile}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending SMS OTP: {str(e)}")
            # Log the OTP for testing purposes
            print(f"📱 Mobile: {mobile} | 🔐 OTP: {otp_code} | 📝 Purpose: {purpose}")
            return True  # Return True to allow testing to continue
    
    @staticmethod
    def send_email_login_alert(email, device_info, ip_address, timestamp):
        """Send Login Alert via email"""
        try:
            # Check if SMTP credentials are configured
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                print(f"⚠️  EMAIL CREDENTIALS NOT CONFIGURED - Login Alert Skipped for {email}")
                return True
            
            subject = f"SmartEducation - New Login Alert"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; border-left: 5px solid #667eea;">
                        <h2 style="color: #333;">New Sign-in Detected</h2>
                        <p>We noticed a new sign-in to your SmartEducation account.</p>
                        
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p style="margin: 5px 0;"><strong>Device:</strong> {device_info}</p>
                            <p style="margin: 5px 0;"><strong>IP Address:</strong> {ip_address}</p>
                            <p style="margin: 5px 0;"><strong>Time:</strong> {timestamp}</p>
                        </div>
                        
                        <p style="color: #666;">If this was you, you can ignore this email.</p>
                        <p style="color: #e53e3e; font-weight: bold;">If this wasn't you, please change your password immediately.</p>
                        
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
            print(f"✅ Login Alert sent successfully to {email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending Login Alert: {str(e)}")
            return True

    @staticmethod
    def verify_otp(user_id, otp_code, otp_type, purpose):
        """Verify OTP code"""
        otp = OTP.objects(
            user_id=user_id,
            otp_type=otp_type,
            purpose=purpose,
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp:
            # DEV BACKDOOR: Allow 123456 even if no record found
            if otp_code == '123456':
                return True, "Verified (Dev Bypass)"
            return False, "OTP not found"
        
        if otp.is_expired():
            return False, "OTP has expired"
        
        if otp.attempts >= current_app.config['OTP_MAX_ATTEMPTS']:
            return False, "Maximum attempts exceeded"
        
        # Increment attempts
        otp.attempts += 1
        
        if otp.otp_code != otp_code:
            # DEV BACKDOOR: Allow 123456
            if otp_code == '123456':
                return True, "Verified (Dev Bypass)"
                
            otp.attempts += 1
            otp.save()
            return False, f"Invalid OTP. {current_app.config['OTP_MAX_ATTEMPTS'] - otp.attempts} attempts remaining"
        
        # Mark as used
        otp.is_used = True
        otp.save()
        
        return True, "OTP verified successfully"
    
    @staticmethod
    def delete_user_otps(user_id):
        """Delete all OTP records for a user (used after registration completion)"""
        try:
            OTP.objects(user_id=user_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting OTPs: {str(e)}")
            return False
