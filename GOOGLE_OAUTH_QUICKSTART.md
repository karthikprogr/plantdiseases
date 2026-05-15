# 🚀 Google OAuth Quick Start Guide

## ⚡ Fast Setup (5 Minutes)

### Step 1: Set Environment Variables (Temporary Testing)

Open PowerShell in the Flask Deployed App folder and run:

```powershell
# Set Google OAuth credentials (replace with your actual credentials)
$env:GOOGLE_CLIENT_ID="YOUR_CLIENT_ID.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET"

# Start the app
python app.py
```

### Step 2: Get Google Credentials

1. Go to: https://console.cloud.google.com/
2. Create new project: "Plant Disease Detection"
3. Go to: APIs & Services > Credentials
4. Create OAuth 2.0 Client ID:
   - Type: Web Application
   - Authorized redirect URIs: `http://127.0.0.1:5000/google-authorize`
5. Copy Client ID and Client Secret
6. Paste them in the PowerShell commands above

### Step 3: Test It!

1. Open browser: http://127.0.0.1:5000
2. Click "Continue with Google"
3. Sign in with your Google account
4. Done! 🎉

## 🔧 Permanent Setup (Using .env file)

### 1. Install python-dotenv

```bash
pip install python-dotenv
```

### 2. Create .env file

Create a file named `.env` in the Flask Deployed App folder:

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
FLASK_SECRET=change-this-to-random-secret-key
```

### 3. Update app.py

Add these lines at the very top of app.py (after the imports):

```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run the app

```bash
python app.py
```

Now the credentials will be loaded automatically from .env file!

## 📋 What You Need from Google Console

Go to: https://console.cloud.google.com/apis/credentials

You need:
1. **Client ID** - Looks like: `123456789-abc123.apps.googleusercontent.com`
2. **Client Secret** - Looks like: `GOCSPX-abc123def456`

### Authorized Redirect URIs (IMPORTANT!)

Add these exact URLs in Google Console:
- `http://localhost:5000/google-authorize`
- `http://127.0.0.1:5000/google-authorize`

## ✅ Features Working

After setup, you'll have:

- ✅ **Login Page**: Google Sign-In button
- ✅ **Signup Page**: Google Sign-Up button
- ✅ **Automatic Account Creation**: First-time Google users get accounts
- ✅ **Secure Authentication**: OAuth 2.0 standard
- ✅ **Email Capture**: User emails stored in database
- ✅ **Username Generation**: Auto-generated from email
- ✅ **Session Management**: Tracks logged-in users
- ✅ **Flash Messages**: Welcome messages for users

## 🎨 UI Updates

### Login Page:
```
┌─────────────────────────────┐
│  [G] Continue with Google   │
│                             │
│          OR                 │
│                             │
│  [Username Field]           │
│  [Password Field]           │
│  [Login Button]             │
└─────────────────────────────┘
```

### Signup Page:
```
┌─────────────────────────────┐
│  [G] Sign up with Google    │
│                             │
│          OR                 │
│                             │
│  [Email Field]              │
│  [Password Field]           │
│  [Sign Up Button]           │
└─────────────────────────────┘
```

## 🐛 Common Issues

### "redirect_uri_mismatch"
**Fix:** Make sure redirect URI in Google Console is exactly:
```
http://127.0.0.1:5000/google-authorize
```

### "invalid_client"
**Fix:** Check that GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are set correctly

### Google button does nothing
**Fix:** Check Flask console for errors. Make sure authlib is installed:
```bash
pip install authlib
```

## 📝 Test User Flow

### New User (First Time):
1. Click "Continue with Google"
2. Choose Google account
3. Grant permissions (email, profile)
4. ✅ Account created automatically
5. ✅ Redirected to home page
6. ✅ Message: "Welcome [Name]! Your account has been created."

### Returning User:
1. Click "Continue with Google"
2. Choose Google account
3. ✅ Logged in automatically
4. ✅ Message: "Welcome back [Name]!"

## 🔒 Security

- ✅ Passwords not stored for Google users
- ✅ Random secure password generated
- ✅ OAuth 2.0 standard protocol
- ✅ Email verified by Google
- ✅ Secure session management
- ✅ No password transmitted to our server

## 📦 Files Modified

- ✅ `templates/login.html` - Added Google button
- ✅ `templates/signup.html` - Added Google button
- ✅ `app.py` - Added OAuth configuration and routes
- ✅ `requirements.txt` - Added authlib dependency

## 🎯 Next Steps

After setup works:
1. Test with different Google accounts
2. Try logging out and back in
3. Make a plant prediction
4. Check that history works
5. Test feedback system

For production deployment, see: `GOOGLE_OAUTH_SETUP.md`

Happy coding! 🌱✨
