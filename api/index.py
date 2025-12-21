
from app import create_app

app = create_app()

# Vercel expects a variable named 'app'
# This file is the entry point for Vercel Serverless Functions
