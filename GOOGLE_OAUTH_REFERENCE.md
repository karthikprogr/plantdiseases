# 🎴 Google OAuth Quick Reference Card

Keep this handy while setting up!

---

## 🔗 Important URLs

| Purpose | URL |
|---------|-----|
| Google Cloud Console | https://console.cloud.google.com/ |
| OAuth Consent Screen | Console → APIs & Services → OAuth consent screen |
| Credentials | Console → APIs & Services → Credentials |
| Your Login Page | http://127.0.0.1:5000/login |
| OAuth Callback | http://127.0.0.1:5000/google-authorize |

---

## 📝 Required Information

### For Google Console:

| Field | Value |
|-------|-------|
| **App Name** | Plant Disease Detection |
| **User Type** | External |
| **Support Email** | your-email@gmail.com |
| **Developer Email** | your-email@gmail.com |
| **Application Type** | Web application |
| **App Name** | Plant Disease Detection Web |

### Scopes (Select These 3):

- ✅ `.../auth/userinfo.email` - View email
- ✅ `.../auth/userinfo.profile` - View profile
- ✅ `openid` - OpenID Connect

### Authorized JavaScript Origins:

```
http://localhost:5000
http://127.0.0.1:5000
```

### Authorized Redirect URIs (EXACT!):

```
http://localhost:5000/google-authorize
http://127.0.0.1:5000/google-authorize
```

---

## 💻 PowerShell Commands

### Set Credentials (Copy-Paste Ready):

```powershell
# Navigate to app folder
cd "c:\Users\DELL\OneDrive\Desktop\Plant-Disease-Detection-main - Copy\Flask Deployed App"

# Set Google credentials (replace with YOUR values!)
$env:GOOGLE_CLIENT_ID="YOUR_CLIENT_ID.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET"

# Verify they're set
Write-Host "Client ID: $env:GOOGLE_CLIENT_ID"
Write-Host "Client Secret: $env:GOOGLE_CLIENT_SECRET"

# Install authlib if not installed
pip install authlib

# Start the app
python app.py
```

### Check If Credentials Are Set:

```powershell
Write-Host $env:GOOGLE_CLIENT_ID
Write-Host $env:GOOGLE_CLIENT_SECRET
```

---

## 🔍 Debug Commands

### Check if authlib is installed:
```powershell
pip show authlib
```

### Check Flask app syntax:
```powershell
python -m py_compile app.py
```

### View environment variables:
```powershell
Get-ChildItem Env: | Where-Object {$_.Name -like "*GOOGLE*"}
```

---

## 🎯 Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **Button does nothing** | `pip install authlib` then restart app |
| **redirect_uri_mismatch** | Add EXACT URI in Google Console |
| **invalid_client** | Check credentials are set: `$env:GOOGLE_CLIENT_ID` |
| **Access blocked** | Add your email as test user in Console |
| **401 Unauthorized** | Restart Flask app after setting credentials |

---

## 📋 Test Checklist (5 Minutes)

1. [ ] Set environment variables
2. [ ] Start Flask app: `python app.py`
3. [ ] Open: http://127.0.0.1:5000/login
4. [ ] See Google button
5. [ ] Click button → Redirects to Google
6. [ ] Sign in → Redirects back
7. [ ] See home page with welcome message

---

## ✅ Success Looks Like

### Google Console:
```
✓ OAuth consent screen: Testing
✓ Test users: 1+ added
✓ OAuth client: Web application created
✓ Redirect URIs: 2 added (localhost + 127.0.0.1)
✓ Credentials: Downloaded/copied
```

### Flask Console:
```
✅ Model loaded successfully
✅ Database tables created successfully
* Running on http://127.0.0.1:5000
127.0.0.1 - - "GET /google-login HTTP/1.1" 302
127.0.0.1 - - "GET /google-authorize?code=... HTTP/1.1" 302
127.0.0.1 - - "GET /home HTTP/1.1" 200
```

### Browser:
```
✓ Login page loads
✓ "Continue with Google" button visible
✓ Button styled with Google colors
✓ Click → Google sign-in page
✓ After sign-in → Your app home page
✓ Flash message: "Welcome [Name]!"
```

---

## 🔐 Credential Format

### Client ID:
```
Format: 123456789012-abcdefghijklmnop.apps.googleusercontent.com
Length: ~70 characters
Contains: Numbers, letters, dashes, dots
Ends with: .apps.googleusercontent.com
```

### Client Secret:
```
Format: GOCSPX-abcd1234efgh5678ijkl
Length: ~30 characters
Starts with: GOCSPX-
Contains: Letters and numbers
```

---

## 📞 Support Resources

| Resource | Location |
|----------|----------|
| **Detailed Setup** | GOOGLE_OAUTH_CONSENT_SCREEN_GUIDE.md |
| **Troubleshooting** | GOOGLE_OAUTH_TROUBLESHOOTING.md |
| **Quick Start** | GOOGLE_OAUTH_QUICKSTART.md |
| **Checklist** | GOOGLE_OAUTH_CHECKLIST.md |
| **Full Docs** | GOOGLE_OAUTH_SETUP.md |

---

## 🚨 Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct |
|---------|----------|
| `google-authorize/` | `google-authorize` |
| `https://127.0.0.1` | `http://127.0.0.1` |
| Missing `:5000` | `127.0.0.1:5000` |
| Trailing spaces in credentials | Exact copy-paste |
| Forgetting to add test user | Add your email first |

---

## 🎨 Button Preview

Your login page will show:

```
╔════════════════════════════════════╗
║  Welcome to Plant Disease          ║
║  Prediction                        ║
║                                    ║
║  ┌──────────────────────────────┐ ║
║  │ [G] Continue with Google     │ ║ ← This button!
║  └──────────────────────────────┘ ║
║                                    ║
║  ─────────── OR ─────────────     ║
║                                    ║
║  [Username]                        ║
║  [Password]                        ║
║  [Login]                           ║
╚════════════════════════════════════╝
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Configure consent screen | 3 minutes |
| Create OAuth client | 2 minutes |
| Set up Flask credentials | 1 minute |
| Test Google login | 1 minute |
| **Total** | **~7 minutes** |

---

## 🎓 Key Concepts

**OAuth 2.0:** Industry-standard protocol for authorization

**Client ID:** Public identifier for your app

**Client Secret:** Private key (keep secret!)

**Redirect URI:** Where Google sends user after authentication

**Scopes:** What data your app can access (email, profile)

**Test Users:** Allowed to use app during "Testing" phase

**Consent Screen:** What users see when granting permissions

---

## 📱 Mobile Support

The Google button is responsive and works on:
- ✅ Desktop browsers
- ✅ Mobile Chrome/Safari
- ✅ Tablets
- ✅ All screen sizes

---

## 🔒 Security Features

- ✅ OAuth 2.0 standard protocol
- ✅ No passwords stored
- ✅ Google handles authentication
- ✅ Secure token exchange
- ✅ Session management
- ✅ HTTPS recommended for production

---

## 💡 Pro Tips

1. **Test with your own email first** before adding others
2. **Keep credentials in .env file** for easy management
3. **Add both localhost and 127.0.0.1** URIs for flexibility
4. **Restart Flask app** after changing credentials
5. **Check Flask console** for detailed error messages
6. **Use incognito mode** to test fresh sign-in experience

---

## 🎉 After Setup

Once working, users can:
- Sign in with Google (1 click)
- Auto-create account (first time)
- No password needed
- Secure authentication
- Fast and convenient

---

**Version:** 1.0  
**Last Updated:** October 13, 2025  
**Status:** Ready for Production ✅

---

**Print this card and keep it handy!** 🖨️
