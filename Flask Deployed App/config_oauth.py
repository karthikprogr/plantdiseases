"""
Google OAuth Configuration
Edit this file with your Google OAuth credentials
"""

# ============================================
# GOOGLE OAUTH CREDENTIALS
# ============================================
# Get these from: https://console.cloud.google.com/apis/credentials
# 
# Steps:
# 1. Go to the URL above
# 2. Create OAuth 2.0 Client ID
# 3. Copy your Client ID and paste below
# 4. Copy your Client Secret and paste below
# 5. Save this file
# 6. Run: python app.py
# ============================================

# Paste your Client ID here (between the quotes)
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"

# Paste your Client Secret here (between the quotes)
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"

# ============================================
# EXAMPLE (this is what it should look like):
# ============================================
# GOOGLE_CLIENT_ID = "PLACEHOLDER_CLIENT_ID.apps.googleusercontent.com"
# GOOGLE_CLIENT_SECRET = "GOCSPX-PLACEHOLDER_SECRET"
# ============================================

# Flask secret key for sessions
FLASK_SECRET_KEY = "plant-disease-detection-secret-key-change-in-production"

# OpenAI API Key (optional - leave as is if you don't have one)
OPENAI_API_KEY = ""
