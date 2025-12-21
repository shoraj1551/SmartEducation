
# 🚀 Vercel Deployment Guide for SmartEducation

**Target**: Deploy Phase 19 (Intelligence Layer) to Production.

## Prerequisites
1.  **Vercel CLI**: `npm i -g vercel`
2.  **MongoDB Atlas**: You must have a cloud database (local MongoDB won't work).
    *   Get your connection string: `mongodb+srv://user:pass@cluster.mongodb.net/SmartEducation`

## Step 1: Login & Initialize
Open your terminal in `SmartEducation` folder:
```powershell
vercel login
vercel link
```

## Step 2: Configure Secrets
Run our helper script to upload your keys (Database URL, Mailtrap, Twilio):
```powershell
./scripts/setup_vercel_secrets.ps1
```
*Alternatively, add them manually in Vercel Dashboard > Settings > Environment Variables.*

## Step 3: Deploy
```powershell
vercel --prod
```

## Troubleshooting
*   **Module Not Found?** Ensure it's in `requirements.txt`.
*   **Database Error?** Check "Whelist IP" in MongoDB Atlas (Allow 0.0.0.0/0 for Vercel).
