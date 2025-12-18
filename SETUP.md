# SmartEducation - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Copy the example file:**
```bash
copy .env.example .env
```

**Edit `.env` and add your credentials:**

#### Mailtrap (Email Testing - FREE)
1. Sign up at https://mailtrap.io
2. Go to: **Email Testing → Inboxes → SMTP Settings**
3. Copy the credentials to your `.env` file:
   ```
   MAIL_USERNAME=your-mailtrap-username
   MAIL_PASSWORD=your-mailtrap-password
   ```

#### Twilio (SMS Service - FREE Trial)
1. Sign up at https://www.twilio.com/try-twilio
2. Go to **Console Dashboard**
3. Copy the credentials to your `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your-account-sid
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_PHONE_NUMBER=your-twilio-phone-number
   ```

#### Generate Secret Keys
```bash
# In Python, generate random secret keys:
python -c "import secrets; print(secrets.token_hex(32))"
```
Add to `.env`:
```
SECRET_KEY=<generated-key>
JWT_SECRET_KEY=<generated-key>
```

### 3. Run the Application

```bash
python app.py
```

The server will start at: **http://localhost:5000**

## Features

### ✅ User Registration
- Name, Email, Mobile Number, Password
- OTP sent to both email and mobile
- Dual verification required

### ✅ Login
- Login with **Email + Password** OR **Mobile + Password**
- JWT token-based authentication

### ✅ Password Reset
- Request reset via email or mobile
- OTP verification for both
- Set new password

### ✅ Security Features
- Passwords hashed with bcrypt
- OTP expires after 10 minutes
- Maximum 3 OTP attempts
- Rate limiting on OTP generation
- JWT session management

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "password": "securepassword"
}
```

#### Verify OTP
```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "user_id": 1,
  "email_otp": "123456",
  "mobile_otp": "654321"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "identifier": "john@example.com",  // or mobile number
  "password": "securepassword"
}
```

#### Forgot Password
```http
POST /api/auth/forgot-password
Content-Type: application/json

{
  "identifier": "john@example.com"  // or mobile number
}
```

#### Reset Password
```http
POST /api/auth/reset-password
Content-Type: application/json

{
  "user_id": 1,
  "email_otp": "123456",
  "mobile_otp": "654321",
  "new_password": "newsecurepassword"
}
```

#### Resend OTP
```http
POST /api/auth/resend-otp
Content-Type: application/json

{
  "user_id": 1,
  "otp_type": "email",  // or "mobile"
  "purpose": "registration"  // or "reset"
}
```

## Testing

### Development Testing
- **Email OTPs**: Check your Mailtrap inbox at https://mailtrap.io
- **SMS OTPs**: Will be sent to the mobile number via Twilio

### Test Flow
1. Open http://localhost:5000
2. Click "Sign Up"
3. Fill in details (use your real email for Mailtrap testing)
4. Check Mailtrap inbox for email OTP
5. Check mobile for SMS OTP
6. Enter both OTPs to verify account
7. Login with email or mobile

## Database

SQLite database is created automatically at `smarteducation.db`

### Tables
- **users**: User accounts
- **otps**: OTP verification codes

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` file to version control
- Change secret keys in production
- Use HTTPS in production
- Configure proper CORS settings for production
- Set up proper rate limiting in production

## Troubleshooting

### Email not sending
- Check Mailtrap credentials in `.env`
- Verify MAIL_USERNAME and MAIL_PASSWORD are correct

### SMS not sending
- Check Twilio credentials in `.env`
- Ensure phone number format includes country code (e.g., +1234567890)
- Verify Twilio account has credits

### Database errors
- Delete `smarteducation.db` and restart app to recreate tables

## Next Steps

After setup:
1. Test registration flow
2. Test login with email
3. Test login with mobile
4. Test password reset
5. Build user dashboard
6. Add course management features
