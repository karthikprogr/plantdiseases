# 🔧 Google OAuth Consent Screen & Client ID Setup - Visual Guide

## 📋 Overview

Before creating OAuth credentials, you must configure the **OAuth Consent Screen**. This is what users see when they sign in with Google.

---

## 🎯 Step 1: Configure OAuth Consent Screen

### 1.1 Navigate to Consent Screen

1. Go to: https://console.cloud.google.com/
2. Select your project: **"Plant Disease Detection"**
3. Click **"APIs & Services"** in left menu
4. Click **"OAuth consent screen"**

### 1.2 Choose User Type

You'll see two options:

```
┌─────────────────────────────────────────┐
│  OAuth Consent Screen Setup             │
│                                          │
│  ○ Internal                             │
│    For users within your organization   │
│    (Requires Google Workspace)          │
│                                          │
│  ● External                             │
│    Available to any test user with     │
│    a Google Account                     │
│                                          │
│         [Continue]                       │
└─────────────────────────────────────────┘
```

**Choose:** ✅ **External** (recommended for most cases)

**Click:** "Create" or "Continue"

---

## 🎯 Step 2: App Information

### 2.1 Required Fields

Fill in the following information:

```
╔════════════════════════════════════════════════╗
║  OAuth Consent Screen - App Information       ║
╠════════════════════════════════════════════════╣
║                                                ║
║  App name *                                    ║
║  ┌──────────────────────────────────────────┐ ║
║  │ Plant Disease Detection                  │ ║
║  └──────────────────────────────────────────┘ ║
║  This name will be shown on consent screen    ║
║                                                ║
║  User support email *                          ║
║  ┌──────────────────────────────────────────┐ ║
║  │ your-email@gmail.com                     │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  App logo (optional)                           ║
║  Upload an image (120x120px recommended)       ║
║                                                ║
║  Application home page (optional)              ║
║  ┌──────────────────────────────────────────┐ ║
║  │ http://127.0.0.1:5000                    │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Application privacy policy link (optional)    ║
║  (Leave blank for development)                 ║
║                                                ║
║  Application terms of service link (optional)  ║
║  (Leave blank for development)                 ║
║                                                ║
╚════════════════════════════════════════════════╝
```

### 2.2 Developer Contact Information

Scroll down and add:

```
╔════════════════════════════════════════════════╗
║  Developer Contact Information *               ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Email addresses (at least one required)       ║
║  ┌──────────────────────────────────────────┐ ║
║  │ your-email@gmail.com                     │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  [+ Add Another Email]                         ║
║                                                ║
╚════════════════════════════════════════════════╝
```

**Click:** "Save and Continue"

---

## 🎯 Step 3: Scopes

### 3.1 Add Required Scopes

You need to specify what information your app will access:

```
╔════════════════════════════════════════════════╗
║  Scopes for Google APIs                        ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Define what data your app can access from     ║
║  users who authenticate with Google            ║
║                                                ║
║  [Add or Remove Scopes]                        ║
║                                                ║
╚════════════════════════════════════════════════╝
```

**Click:** "Add or Remove Scopes"

A dialog will open:

```
╔════════════════════════════════════════════════╗
║  Update selected scopes                        ║
╠════════════════════════════════════════════════╣
║  Filter: [search...]                           ║
║                                                ║
║  ☑ .../auth/userinfo.email                    ║
║    View your email address                     ║
║                                                ║
║  ☑ .../auth/userinfo.profile                  ║
║    See your personal info                      ║
║                                                ║
║  ☑ openid                                      ║
║    Associate you with your personal info       ║
║                                                ║
║  [ ] .../auth/gmail.readonly                   ║
║    (Don't select this - not needed)            ║
║                                                ║
║         [Cancel]  [Update]                     ║
╚════════════════════════════════════════════════╝
```

**Select these THREE scopes:**
- ✅ `.../auth/userinfo.email` - View email address
- ✅ `.../auth/userinfo.profile` - See personal info
- ✅ `openid` - Associate with personal info

**Click:** "Update"

**Click:** "Save and Continue"

---

## 🎯 Step 4: Test Users

### 4.1 Add Test Users (Required for External Apps)

Since your app is "External" and not published, you must add test users:

```
╔════════════════════════════════════════════════╗
║  Test Users                                    ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Add email addresses for users who can test    ║
║  your app before publishing                    ║
║                                                ║
║  [+ Add Users]                                 ║
║                                                ║
║  Test Users:                                   ║
║  • your-email@gmail.com                        ║
║  • friend-email@gmail.com                      ║
║                                                ║
╚════════════════════════════════════════════════╝
```

**Click:** "+ Add Users"

**Enter:** Your email address(es) - one per line

**Click:** "Save and Continue"

---

## 🎯 Step 5: Summary & Verification

Review your configuration:

```
╔════════════════════════════════════════════════╗
║  Summary                                       ║
╠════════════════════════════════════════════════╣
║                                                ║
║  App name: Plant Disease Detection             ║
║  User support email: your@email.com            ║
║  Scopes: 3 selected                            ║
║  Test users: 1-5 added                         ║
║                                                ║
║  Publishing status: Testing                    ║
║                                                ║
║         [Back to Dashboard]                    ║
╚════════════════════════════════════════════════╝
```

**Click:** "Back to Dashboard"

✅ **OAuth Consent Screen is now configured!**

---

## 🎯 Step 6: Create OAuth Client ID

Now you can create the actual credentials:

### 6.1 Go to Credentials

1. Click **"Credentials"** in the left menu
2. Click **"+ Create Credentials"** at the top
3. Select **"OAuth client ID"**

### 6.2 Choose Application Type

```
╔════════════════════════════════════════════════╗
║  Create OAuth client ID                        ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Application type *                            ║
║  ┌──────────────────────────────────────────┐ ║
║  │ ● Web application                        │ ║
║  │ ○ Android                                │ ║
║  │ ○ Chrome app                             │ ║
║  │ ○ iOS                                    │ ║
║  │ ○ Desktop app                            │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
╚════════════════════════════════════════════════╝
```

**Select:** ✅ **Web application**

### 6.3 Configure Web Application

```
╔════════════════════════════════════════════════╗
║  Web application                               ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Name *                                        ║
║  ┌──────────────────────────────────────────┐ ║
║  │ Plant Disease Detection Web              │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  Authorized JavaScript origins                 ║
║  ┌──────────────────────────────────────────┐ ║
║  │ http://localhost:5000                    │ ║
║  │ http://127.0.0.1:5000                    │ ║
║  └──────────────────────────────────────────┘ ║
║  [+ Add URI]                                   ║
║                                                ║
║  Authorized redirect URIs *                    ║
║  ┌──────────────────────────────────────────┐ ║
║  │ http://localhost:5000/google-authorize  │ ║
║  │ http://127.0.0.1:5000/google-authorize  │ ║
║  └──────────────────────────────────────────┘ ║
║  [+ Add URI]                                   ║
║                                                ║
║         [Cancel]  [Create]                     ║
╚════════════════════════════════════════════════╝
```

**Fill in:**

1. **Name:** `Plant Disease Detection Web`

2. **Authorized JavaScript origins:**
   - `http://localhost:5000`
   - `http://127.0.0.1:5000`

3. **Authorized redirect URIs:** ⚠️ **CRITICAL - Must be exact!**
   - `http://localhost:5000/google-authorize`
   - `http://127.0.0.1:5000/google-authorize`

**Click:** "Create"

---

## 🎯 Step 7: Save Your Credentials

You'll see a popup with your credentials:

```
╔════════════════════════════════════════════════╗
║  OAuth client created                          ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Your Client ID                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 123456789-abc123def456.apps.google...   │ ║
║  └──────────────────────────────────────────┘ ║
║  [Copy] 📋                                     ║
║                                                ║
║  Your Client Secret                            ║
║  ┌──────────────────────────────────────────┐ ║
║  │ GOCSPX-abc123def456ghi789jkl012         │ ║
║  └──────────────────────────────────────────┘ ║
║  [Copy] 📋                                     ║
║                                                ║
║  ⚠️ Keep these credentials secure!             ║
║                                                ║
║         [OK]                                   ║
╚════════════════════════════════════════════════╝
```

**IMPORTANT:** 
1. ✅ **Copy the Client ID** - Click copy button
2. ✅ **Copy the Client Secret** - Click copy button
3. ✅ **Save them somewhere safe** (text file, password manager)

**Click:** "OK"

---

## 🎯 Step 8: Configure Your Flask App

Now use these credentials in your application:

### Option A: Set Environment Variables (Quick Test)

**PowerShell:**
```powershell
# Paste YOUR actual credentials here
$env:GOOGLE_CLIENT_ID="123456789-abc123def456.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="GOCSPX-abc123def456ghi789jkl012"

# Run the app
cd "c:\Users\DELL\OneDrive\Desktop\Plant-Disease-Detection-main - Copy\Flask Deployed App"
python app.py
```

### Option B: Create .env File (Recommended)

1. Create file: `.env` in Flask Deployed App folder

2. Add your credentials:
```env
GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456ghi789jkl012
FLASK_SECRET=your-random-secret-key-here
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

4. Add to top of `app.py` (after imports):
```python
from dotenv import load_dotenv
load_dotenv()
```

5. Run the app:
```bash
python app.py
```

---

## 🧪 Step 9: Test Google Login

1. **Start your Flask app:**
   ```bash
   python app.py
   ```

2. **Open browser:**
   ```
   http://127.0.0.1:5000/login
   ```

3. **Click:** "Continue with Google" button

4. **Select your Google account**

5. **Review permissions:**
   ```
   ╔════════════════════════════════════════╗
   ║  Plant Disease Detection wants to:    ║
   ╠════════════════════════════════════════╣
   ║  ✓ View your email address            ║
   ║  ✓ See your personal info             ║
   ║                                        ║
   ║    [Cancel]  [Continue]                ║
   ╚════════════════════════════════════════╝
   ```

6. **Click:** "Continue"

7. **You should be redirected back and logged in!** ✅

---

## ✅ Success Indicators

If everything works, you'll see:

1. **In Flask console:**
   ```
   127.0.0.1 - - [13/Oct/2025 23:00:00] "GET /google-login HTTP/1.1" 302 -
   127.0.0.1 - - [13/Oct/2025 23:00:01] "GET /google-authorize?code=... HTTP/1.1" 302 -
   127.0.0.1 - - [13/Oct/2025 23:00:01] "GET /home HTTP/1.1" 200 -
   ```

2. **In browser:**
   - Redirected to home page
   - Flash message: "Welcome [Your Name]! Your account has been created."
   - Logged in successfully

---

## 🐛 Common Issues & Solutions

### Issue 1: "redirect_uri_mismatch"

**Error:**
```
Error 400: redirect_uri_mismatch
The redirect URI in the request, http://127.0.0.1:5000/google-authorize, 
does not match the ones authorized for the OAuth client.
```

**Solution:**
1. Go back to Google Console → Credentials
2. Click on your OAuth client ID
3. Under "Authorized redirect URIs", add EXACTLY:
   - `http://127.0.0.1:5000/google-authorize`
4. Make sure there's no trailing slash
5. Save and try again

### Issue 2: "Access blocked: This app's request is invalid"

**Error:**
```
Access blocked: Plant Disease Detection's request is invalid
```

**Solution:**
1. Go to OAuth consent screen
2. Add yourself as a test user
3. Make sure app status is "Testing"
4. Try again with the email you added

### Issue 3: "invalid_client"

**Error in Flask console:**
```
invalid_client: Unauthorized
```

**Solution:**
1. Check that GOOGLE_CLIENT_ID is set correctly
2. Check that GOOGLE_CLIENT_SECRET is set correctly
3. Make sure you copied them completely (no spaces, no line breaks)
4. Restart Flask app after setting variables

### Issue 4: Credentials Not Loading

**Symptom:** Button does nothing, or error about "YOUR_GOOGLE_CLIENT_ID"

**Solution:**
1. Check environment variables are set in the same terminal/session
2. If using .env file, make sure python-dotenv is installed
3. Make sure .env file is in the correct directory (Flask Deployed App folder)
4. Restart the Flask app

---

## 📝 Quick Checklist

Before testing, verify:

- [ ] OAuth Consent Screen configured
- [ ] App name: "Plant Disease Detection"
- [ ] User type: External
- [ ] Scopes: email, profile, openid (3 total)
- [ ] Test users added (your email)
- [ ] OAuth Client ID created
- [ ] Application type: Web application
- [ ] Redirect URIs added correctly
- [ ] Client ID copied and saved
- [ ] Client Secret copied and saved
- [ ] Environment variables set OR .env file created
- [ ] Flask app restarted with credentials
- [ ] Testing with email added as test user

---

## 🎉 You're All Set!

Once configured, your users can:
- ✅ Sign in with Google in one click
- ✅ No password to remember
- ✅ Automatic account creation
- ✅ Secure OAuth 2.0 authentication

**Next Steps:**
1. Test with your Google account
2. Add more test users if needed
3. Make some plant predictions!
4. When ready for production, publish the OAuth consent screen

---

## 📚 Additional Resources

- **Google OAuth Documentation:** https://developers.google.com/identity/protocols/oauth2
- **OAuth Consent Screen Help:** https://support.google.com/cloud/answer/10311615
- **Authlib Documentation:** https://docs.authlib.org/

**Need help?** Check the Flask console logs for detailed error messages!

Happy coding! 🌱✨
