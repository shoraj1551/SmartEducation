# Instructions for Adding Your Credentials

## Step 1: Copy the .env.example file

In your terminal, run:
```bash
copy .env.example .env
```

## Step 2: Get Mailtrap Credentials (Email Testing)

1. Go to https://mailtrap.io
2. Click "Sign Up" (it's FREE)
3. After signing in, go to "Email Testing" → "Inboxes"
4. Click on your inbox (or create one)
5. Click on "SMTP Settings"
6. You'll see:
   - **Host**: sandbox.smtp.mailtrap.io
   - **Port**: 2525
   - **Username**: (copy this)
   - **Password**: (copy this)

7. Open your `.env` file and update:
   ```
   MAIL_USERNAME=paste-your-username-here
   MAIL_PASSWORD=paste-your-password-here
   ```

## Step 3: Get Twilio Credentials (SMS Service)

1. Go to https://www.twilio.com/try-twilio
2. Click "Sign up and start building" (FREE trial with credits)
3. Complete the verification process
4. After signing in, you'll see your Dashboard with:
   - **Account SID**: (copy this)
   - **Auth Token**: (click to reveal and copy)

5. Get a phone number:
   - Click "Get a Twilio phone number"
   - Accept the suggested number (or choose your own)
   - Copy this number

6. Open your `.env` file and update:
   ```
   TWILIO_ACCOUNT_SID=paste-your-account-sid-here
   TWILIO_AUTH_TOKEN=paste-your-auth-token-here
   TWILIO_PHONE_NUMBER=paste-your-phone-number-here
   ```
   (Phone number format: +1234567890)

## Step 4: Generate Secret Keys

In your terminal, run this command TWICE to generate two different keys:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy each generated key and update your `.env` file:
```
SECRET_KEY=paste-first-generated-key-here
JWT_SECRET_KEY=paste-second-generated-key-here
```

## Step 5: Verify Your .env File

Your `.env` file should now look like this (with your actual values):
```
# Application Settings
APP_NAME=SmartEducation
APP_ENV=development
DEBUG=True
SECRET_KEY=your-actual-secret-key-here
JWT_SECRET_KEY=your-actual-jwt-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///smarteducation.db

# Server Configuration
HOST=localhost
PORT=5000

# MAILTRAP - Email Testing
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-actual-mailtrap-username
MAIL_PASSWORD=your-actual-mailtrap-password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=noreply@smarteducation.com

# TWILIO - SMS Service
TWILIO_ACCOUNT_SID=your-actual-account-sid
TWILIO_AUTH_TOKEN=your-actual-auth-token
TWILIO_PHONE_NUMBER=your-actual-phone-number

# OTP Configuration
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=3
OTP_RATE_LIMIT_SECONDS=60
```

## Step 6: Install Dependencies and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## ✅ You're Done!

The application will be running at: **http://localhost:5000**

Test it by:
1. Clicking "Sign Up"
2. Filling in your details
3. Checking Mailtrap inbox for email OTP
4. Checking your mobile for SMS OTP

---

**Need Help?**
- Mailtrap not working? Double-check username and password
- Twilio not working? Verify Account SID, Auth Token, and phone number format
- Still stuck? Check the SETUP.md file for more details
