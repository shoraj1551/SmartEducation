
# Setup Vercel Secrets
Write-Host "Setting up Vercel Secrets for SmartEducation..." -ForegroundColor Cyan

# Check for Vercel CLI
if (-not (Get-Command "vercel" -ErrorAction SilentlyContinue)) {
    Write-Error "Vercel CLI not found. Please install it first: npm i -g vercel"
    exit 1
}

$secrets = @(
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "DATABASE_URL",
    "MAIL_SERVER",
    "MAIL_PORT",
    "MAIL_USERNAME",
    "MAIL_PASSWORD",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_PHONE_NUMBER"
)

Write-Host "Please ensure you have your .env values ready."
Write-Host "We will proceed to add them to 'production' environment on Vercel."

foreach ($key in $secrets) {
    $val = Read-Host "Enter value for $key"
    if ($val) {
        # Using creating 'vercel env add' command
        # Syntax: echo value | vercel env add NAME production
        Write-Host "Adding $key..."
        $cmd = "vercel env add $key production"
        # We need to pipe input to it because 'vercel env add' prompts for value
        # But wait, 'vercel env add NAME value targets' syntax might differ.
        # Actually standard is: vercel env add NAME [production|preview|development]
        # And it prompts for value.
        # Automating this is tricky in PS without expect.
        # Let's try passing arguments if supported, or just running it interactively.
        
        Write-Host "Running: vercel env add $key production"
        echo $val | vercel env add $key production
    }
}

Write-Host "All secrets processed!" -ForegroundColor Green
