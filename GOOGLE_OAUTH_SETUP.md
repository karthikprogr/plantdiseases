# Google OAuth Setup Guide

## 📋 Prerequisites
- Google Account
- Google Cloud Console access

## 🔧 Step-by-Step Setup

### 1. Create Google OAuth Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project (or select existing)**
   - Click on project dropdown at top
   - Click "New Project"
   - Name: "Plant Disease Detection"
   - Click "Create"

3. **Enable Google+ API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click on it and press "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: External (for testing) or Internal (for organization)
     - App name: Plant Disease Detection
     - User support email: Your email
     - Developer contact: Your email
     - Click "Save and Continue"
     - Scopes: Add email, profile, openid (click "Add or Remove Scopes")
     - Test users: Add your email for testing
     - Click "Save and Continue"
   
5. **Configure OAuth Client ID**
   - Application type: "Web application"
   - Name: "Plant Disease Detection Web"
   - Authorized JavaScript origins:
     - http://localhost:5000
     - http://127.0.0.1:5000
   - Authorized redirect URIs:
     - http://localhost:5000/google-authorize
     - http://127.0.0.1:5000/google-authorize
   - Click "Create"

6. **Copy Credentials**
   - You'll see "Client ID" and "Client Secret"
   - **IMPORTANT:** Copy these values! You'll need them next.

### 2. Configure Application

#### Option A: Using Environment Variables (Recommended for Production)

**Windows (PowerShell):**
```powershell
$env:GOOGLE_CLIENT_ID="your-client-id-here.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="your-client-secret-here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
set GOOGLE_CLIENT_SECRET=your-client-secret-here
```

**Linux/Mac:**
```bash
export GOOGLE_CLIENT_ID="your-client-id-here.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret-here"
```

#### Option B: Using .env File (Recommended for Development)

1. Create a `.env` file in the Flask Deployed App folder:

```env
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
FLASK_SECRET=your-random-secret-key-here
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Add to the top of app.py (after imports):
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Option C: Direct Configuration (NOT recommended for production)

Edit `app.py` and replace:
```python
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
```

With your actual credentials:
```python
app.config['GOOGLE_CLIENT_ID'] = 'your-actual-client-id.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = 'your-actual-client-secret'
```

### 3. Run the Application

```bash
cd "Flask Deployed App"
python app.py
```

### 4. Test Google Login

1. Open browser: http://127.0.0.1:5000
2. You should see the login page with "Continue with Google" button
3. Click "Continue with Google"
4. Select your Google account
5. Grant permissions (email, profile)
6. You should be redirected back and logged in!

## 🔒 Security Notes

### For Development:
- Use localhost/127.0.0.1 URLs
- Keep credentials in .env file (add .env to .gitignore)
- Test users must be added in OAuth consent screen

### For Production:
- Use environment variables on server
- Add production domain to authorized origins/redirect URIs
- Switch OAuth consent screen to "Production" mode
- Use HTTPS (required for production OAuth)
- Never commit credentials to Git

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
**Solution:** Make sure redirect URI in Google Console exactly matches:
- http://127.0.0.1:5000/google-authorize (for development)

### Error: "invalid_client"
**Solution:** 
- Check that GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are set correctly
- Verify credentials are from the same OAuth client

### Error: "Access blocked: This app's request is invalid"
**Solution:**
- Make sure OAuth consent screen is configured
- Add your email as a test user
- Enable required APIs (Google+ API)

### Google button doesn't work
**Solution:**
- Check Flask console for errors
- Verify authlib is installed: `pip list | grep authlib`
- Check that /google-login route exists

## 📝 Database Schema

Google authenticated users are stored with:
- **username**: Auto-generated from email (before @)
- **email**: Google email address
- **password_hash**: Random secure password (not used for Google login)
- **is_active**: True by default

Users can login with:
1. Google OAuth (if account created via Google)
2. Username/Password (if account created via Signup form)

## 🎨 UI Features

The login page now includes:
- ✅ Google Sign-In button with official Google colors
- ✅ "OR" divider between Google and traditional login
- ✅ Maintains existing username/password login
- ✅ Mobile-responsive design
- ✅ Smooth animations and hover effects

## 📱 User Experience Flow

### New User (First Time Google Login):
1. Click "Continue with Google"
2. Select Google account
3. Grant permissions
4. Account automatically created
5. Redirected to home page
6. Flash message: "Welcome [Name]! Your account has been created."

### Returning User (Google Login):
1. Click "Continue with Google"
2. Select Google account
3. Automatically logged in
4. Redirected to home page
5. Flash message: "Welcome back [Name]!"

## ✅ Features Implemented

- ✅ Google OAuth 2.0 integration
- ✅ Automatic user account creation
- ✅ Secure session management
- ✅ Email-based user identification
- ✅ Username conflict resolution
- ✅ Last login tracking
- ✅ Error handling and flash messages
- ✅ Beautiful UI with Google branding
- ✅ Mobile responsive design
- ✅ Backward compatible with existing auth

## 🚀 Next Steps (Optional Enhancements)

1. **Profile Pictures**: Store Google profile picture URL
2. **Email Verification**: Verify email for username/password signups
3. **Account Linking**: Link Google account to existing username/password account
4. **Social Sharing**: Use Google account for social features
5. **Multiple OAuth Providers**: Add Facebook, GitHub, Microsoft login
6. **Two-Factor Authentication**: Add 2FA for username/password accounts

## 📞 Support

If you encounter issues:
1. Check Flask console logs for detailed error messages
2. Verify Google Console configuration
3. Test with a different Google account
4. Check that all required packages are installed
5. Clear browser cookies/cache and try again

Happy coding! 🌱✨
