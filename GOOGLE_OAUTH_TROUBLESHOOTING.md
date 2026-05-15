# 🔍 Google OAuth Troubleshooting Flowchart

## 🚦 Quick Diagnosis

Follow this flowchart to solve your OAuth issues:

---

## Problem 1: "Configure Consent Screen" Message

```
┌─────────────────────────────────────────────┐
│ You see: "To create an OAuth client ID,    │
│ you must first configure your consent       │
│ screen"                                     │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Solution: Configure OAuth Consent Screen    │
├─────────────────────────────────────────────┤
│ 1. Go to APIs & Services                    │
│ 2. Click "OAuth consent screen"             │
│ 3. Select "External"                        │
│ 4. Fill in app name & email                 │
│ 5. Add scopes (email, profile, openid)      │
│ 6. Add test users                           │
│ 7. Save and continue                        │
└─────────────────────────────────────────────┘
                    │
                    ▼
        ✅ Now create OAuth Client ID
```

---

## Problem 2: "redirect_uri_mismatch" Error

```
┌─────────────────────────────────────────────┐
│ Error 400: redirect_uri_mismatch            │
│ The redirect URI does not match...          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Check: What URI are you using?              │
└─────────────────────────────────────────────┘
       │                           │
       ▼                           ▼
  localhost:5000            127.0.0.1:5000
       │                           │
       ▼                           ▼
┌──────────────────┐      ┌──────────────────┐
│ Add to Console:  │      │ Add to Console:  │
│                  │      │                  │
│ http://localhost │      │ http://127.0.0.1 │
│ :5000/google-    │      │ :5000/google-    │
│ authorize        │      │ authorize        │
└──────────────────┘      └──────────────────┘
       │                           │
       └───────────┬───────────────┘
                   ▼
         ✅ Save and try again
```

---

## Problem 3: "Access blocked" Error

```
┌─────────────────────────────────────────────┐
│ Access blocked: This app's request is       │
│ invalid                                     │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Is your email added as test user?          │
└─────────────────────────────────────────────┘
       │                           │
       ▼ NO                        ▼ YES
┌──────────────────┐      ┌──────────────────┐
│ 1. Go to OAuth   │      │ Check publishing │
│    consent screen│      │ status           │
│ 2. Click "Test   │      │                  │
│    users"        │      │ Should be:       │
│ 3. Add your email│      │ "Testing"        │
│ 4. Save          │      │                  │
└──────────────────┘      └──────────────────┘
       │                           │
       └───────────┬───────────────┘
                   ▼
         ✅ Try signing in again
```

---

## Problem 4: "invalid_client" Error

```
┌─────────────────────────────────────────────┐
│ Flask console shows:                         │
│ invalid_client: Unauthorized                 │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Are credentials set correctly?               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Check in PowerShell:                         │
│ $env:GOOGLE_CLIENT_ID                        │
│ $env:GOOGLE_CLIENT_SECRET                    │
└─────────────────────────────────────────────┘
       │                           │
       ▼ Shows values?             ▼ Empty/Not set?
       │                           │
       ▼                           ▼
┌──────────────────┐      ┌──────────────────┐
│ Verify values    │      │ Set them:        │
│ match Google     │      │                  │
│ Console exactly  │      │ $env:GOOGLE_     │
│                  │      │ CLIENT_ID="..."  │
│ No extra spaces  │      │                  │
│ Complete copy    │      │ $env:GOOGLE_     │
└──────────────────┘      │ CLIENT_SECRET    │
                          │ ="..."           │
                          └──────────────────┘
       │                           │
       └───────────┬───────────────┘
                   ▼
         ✅ Restart Flask app
```

---

## Problem 5: Google Button Does Nothing

```
┌─────────────────────────────────────────────┐
│ Clicking "Continue with Google" does        │
│ nothing                                     │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Check Flask console for errors              │
└─────────────────────────────────────────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    ModuleNotFoundError    Route not found
          │                   │
          ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ Install authlib: │  │ Check app.py has:│
│                  │  │                  │
│ pip install      │  │ @app.route(      │
│ authlib          │  │ '/google-login') │
│                  │  │                  │
│ Restart app      │  │ @app.route(      │
└──────────────────┘  │ '/google-        │
                      │ authorize')      │
                      └──────────────────┘
          │                   │
          └─────────┬─────────┘
                    ▼
          ✅ Should work now
```

---

## Problem 6: Works on Localhost but Not 127.0.0.1

```
┌─────────────────────────────────────────────┐
│ Works on: http://localhost:5000             │
│ Fails on: http://127.0.0.1:5000             │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ Add BOTH redirect URIs in Google Console:   │
├─────────────────────────────────────────────┤
│ 1. http://localhost:5000/google-authorize   │
│ 2. http://127.0.0.1:5000/google-authorize   │
└─────────────────────────────────────────────┘
                    │
                    ▼
          ✅ Both will work now
```

---

## ✅ Success Checklist

Use this to verify everything is set up correctly:

```
OAuth Consent Screen:
├─ [ ] App name set
├─ [ ] Support email set
├─ [ ] Scopes added (email, profile, openid)
├─ [ ] Test users added (your email)
└─ [ ] Status: Testing

OAuth Client ID:
├─ [ ] Type: Web application
├─ [ ] Name set
├─ [ ] JavaScript origins added
├─ [ ] Redirect URIs added (both localhost & 127.0.0.1)
├─ [ ] Client ID copied
└─ [ ] Client Secret copied

Flask Application:
├─ [ ] authlib installed
├─ [ ] GOOGLE_CLIENT_ID set
├─ [ ] GOOGLE_CLIENT_SECRET set
├─ [ ] App restarted with credentials
├─ [ ] /google-login route exists
├─ [ ] /google-authorize route exists
└─ [ ] No console errors

Testing:
├─ [ ] Using test user email
├─ [ ] Browser allows cookies
├─ [ ] No VPN blocking OAuth
└─ [ ] Correct URL (localhost or 127.0.0.1)
```

---

## 🎯 Most Common Mistake

### ❌ Wrong Redirect URI Format

**Incorrect:**
- `http://127.0.0.1:5000/google-authorize/` (trailing slash)
- `http://127.0.0.1:5000google-authorize` (missing slash)
- `https://127.0.0.1:5000/google-authorize` (https instead of http)
- `http://127.0.0.1/google-authorize` (missing :5000)

**Correct:**
- ✅ `http://127.0.0.1:5000/google-authorize`
- ✅ `http://localhost:5000/google-authorize`

---

## 🆘 Still Not Working?

### Debug Steps:

1. **Check Flask Console**
   ```
   Look for errors starting with:
   - "redirect_uri_mismatch"
   - "invalid_client"
   - "ModuleNotFoundError"
   ```

2. **Check Browser Console (F12)**
   ```
   Look for JavaScript errors or network failures
   ```

3. **Verify Environment**
   ```powershell
   # Check if variables are set
   Write-Host $env:GOOGLE_CLIENT_ID
   Write-Host $env:GOOGLE_CLIENT_SECRET
   ```

4. **Test Manually**
   ```
   Visit: http://127.0.0.1:5000/google-login
   Should redirect to Google
   ```

5. **Check Google Console**
   ```
   APIs & Services → Credentials
   Click on your OAuth client
   Verify all settings
   ```

---

## 📞 Getting Help

If still stuck, gather this information:

```
1. Error message (exact text)
2. Flask console output
3. Browser console errors (F12)
4. Screenshot of Google Console redirect URIs
5. Which URL you're using (localhost or 127.0.0.1)
6. Whether credentials are set (don't share actual values!)
```

---

## 🎉 Working Configuration Example

When everything is correct, you should see:

**Google Console:**
```
OAuth Client ID: 123456...apps.googleusercontent.com
Client Secret: GOCSPX-abc123...
Redirect URIs:
  - http://localhost:5000/google-authorize
  - http://127.0.0.1:5000/google-authorize
```

**PowerShell:**
```powershell
$env:GOOGLE_CLIENT_ID="123456...apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="GOCSPX-abc123..."
```

**Flask Console:**
```
* Running on http://127.0.0.1:5000
127.0.0.1 - - [13/Oct/2025] "GET /google-login" 302
127.0.0.1 - - [13/Oct/2025] "GET /google-authorize?code=..." 302
127.0.0.1 - - [13/Oct/2025] "GET /home" 200
```

**Browser:**
```
✅ Redirected to home page
✅ Flash message: "Welcome [Name]!"
✅ Logged in successfully
```

That's it! 🚀
