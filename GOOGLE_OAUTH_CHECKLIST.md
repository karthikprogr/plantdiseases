# ✅ Google OAuth Setup Checklist

Print this and check off each step as you complete it!

---

## Part 1: Google Cloud Console Setup

### Step 1: Create Project
- [ ] Go to: https://console.cloud.google.com/
- [ ] Create new project: "Plant Disease Detection"
- [ ] Select the project

### Step 2: Configure OAuth Consent Screen
- [ ] Go to: APIs & Services → OAuth consent screen
- [ ] Select: **External**
- [ ] Click: Create/Continue

#### App Information:
- [ ] App name: **Plant Disease Detection**
- [ ] User support email: **your-email@gmail.com**
- [ ] Developer contact: **your-email@gmail.com**
- [ ] Click: Save and Continue

#### Scopes:
- [ ] Click: Add or Remove Scopes
- [ ] Check: ☑ `.../auth/userinfo.email`
- [ ] Check: ☑ `.../auth/userinfo.profile`
- [ ] Check: ☑ `openid`
- [ ] Click: Update
- [ ] Click: Save and Continue

#### Test Users:
- [ ] Click: + Add Users
- [ ] Add your email: **_________________@gmail.com**
- [ ] Click: Save and Continue
- [ ] Review summary
- [ ] Click: Back to Dashboard

### Step 3: Create OAuth Client ID
- [ ] Go to: APIs & Services → Credentials
- [ ] Click: + Create Credentials
- [ ] Select: OAuth client ID
- [ ] Application type: **Web application**
- [ ] Name: **Plant Disease Detection Web**

#### Authorized JavaScript origins:
- [ ] Add: `http://localhost:5000`
- [ ] Add: `http://127.0.0.1:5000`

#### Authorized redirect URIs: ⚠️ CRITICAL!
- [ ] Add: `http://localhost:5000/google-authorize`
- [ ] Add: `http://127.0.0.1:5000/google-authorize`
- [ ] Double-check: No trailing slashes!
- [ ] Click: Create

### Step 4: Save Credentials
- [ ] Copy Client ID: ____________________________________________
- [ ] Copy Client Secret: ________________________________________
- [ ] Save them in a safe place!

---

## Part 2: Flask Application Setup

### Step 1: Install Dependencies
```powershell
cd "c:\Users\DELL\OneDrive\Desktop\Plant-Disease-Detection-main - Copy\Flask Deployed App"
```

- [ ] Run: `pip install authlib`
- [ ] Verify: No errors

### Step 2: Set Environment Variables

#### Option A: PowerShell (Quick Test)
```powershell
$env:GOOGLE_CLIENT_ID="YOUR_CLIENT_ID_HERE"
$env:GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"
```

- [ ] Paste YOUR Client ID
- [ ] Paste YOUR Client Secret
- [ ] Press Enter

#### Option B: .env File (Recommended)
- [ ] Create file: `.env` in Flask Deployed App folder
- [ ] Add:
  ```
  GOOGLE_CLIENT_ID=your_client_id_here
  GOOGLE_CLIENT_SECRET=your_client_secret_here
  ```
- [ ] Install: `pip install python-dotenv`
- [ ] Add to app.py top:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```

### Step 3: Start Flask App
- [ ] Run: `python app.py`
- [ ] Wait for: "Running on http://127.0.0.1:5000"
- [ ] No errors in console

---

## Part 3: Testing

### Step 1: Open Login Page
- [ ] Open browser: `http://127.0.0.1:5000/login`
- [ ] Page loads successfully
- [ ] See "Continue with Google" button

### Step 2: Test Google Sign-In
- [ ] Click: "Continue with Google"
- [ ] Redirected to Google sign-in
- [ ] Select your Google account (must be test user!)
- [ ] Review permissions screen
- [ ] Click: Continue

### Step 3: Verify Success
- [ ] Redirected back to your app
- [ ] See home page
- [ ] See flash message: "Welcome [Name]!"
- [ ] Check Flask console: No errors

### Step 4: Test Again (Returning User)
- [ ] Logout from app
- [ ] Click "Continue with Google" again
- [ ] Should login immediately (no permission screen)
- [ ] See: "Welcome back [Name]!"

---

## ✅ Success Indicators

If everything works, you'll see:

**In Browser:**
```
✅ Login page has Google button
✅ Button is styled with Google colors
✅ Clicking button redirects to Google
✅ After login, redirected to home page
✅ Flash message appears
✅ Username shown in navbar
```

**In Flask Console:**
```
✅ No errors
✅ GET /google-login → 302 redirect
✅ GET /google-authorize?code=... → 302 redirect
✅ GET /home → 200 OK
```

**In Database:**
```
✅ New user created (check with DB browser)
✅ Email stored
✅ Username generated from email
✅ Last login updated
```

---

## ❌ Common Issues

### Issue 1: Button Does Nothing
- [ ] Check: authlib installed?
- [ ] Check: Flask console for errors
- [ ] Check: Browser console (F12) for errors

### Issue 2: "redirect_uri_mismatch"
- [ ] Verify redirect URI in Google Console matches EXACTLY
- [ ] No trailing slash
- [ ] Correct port (:5000)
- [ ] Correct protocol (http://)

### Issue 3: "invalid_client"
- [ ] Check: Environment variables set?
- [ ] Verify: No typos in credentials
- [ ] Try: Restart Flask app

### Issue 4: "Access blocked"
- [ ] Verify: Your email is added as test user
- [ ] Check: OAuth consent screen configured
- [ ] Try: Different Google account (that's a test user)

---

## 📋 Pre-Flight Checklist

Before asking for help, verify:

- [ ] OAuth consent screen shows "Testing" status
- [ ] Your email is in test users list
- [ ] Client ID and Secret are set correctly
- [ ] Redirect URIs in Google Console match app code
- [ ] authlib is installed
- [ ] Flask app restarted after setting credentials
- [ ] Using email that's added as test user
- [ ] No VPN or proxy blocking OAuth

---

## 🎉 All Done!

When all checkboxes are checked:
- ✅ Google OAuth is fully configured
- ✅ Users can sign in with Google
- ✅ Accounts created automatically
- ✅ Secure authentication working

**Congratulations!** 🚀

---

## 📚 Need Help?

Refer to these guides:
1. `GOOGLE_OAUTH_CONSENT_SCREEN_GUIDE.md` - Detailed visual guide
2. `GOOGLE_OAUTH_TROUBLESHOOTING.md` - Flowcharts for debugging
3. `GOOGLE_OAUTH_QUICKSTART.md` - Fast setup instructions
4. `GOOGLE_OAUTH_SETUP.md` - Complete documentation

---

## 🔐 Security Reminder

- [ ] Never commit credentials to Git
- [ ] Add .env to .gitignore
- [ ] Keep Client Secret secure
- [ ] Use environment variables in production
- [ ] Enable HTTPS in production

---

**Date Completed:** ____________

**Tested By:** ____________

**Notes:**
_________________________________
_________________________________
_________________________________
