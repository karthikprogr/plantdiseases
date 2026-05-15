# 🎯 QUICK START - Google Sign-In (Super Simple!)

## 📋 What You Need

From Google Cloud Console, you should have:
- ✅ Client ID (looks like: `123456...apps.googleusercontent.com`)
- ✅ Client Secret (looks like: `GOCSPX-abc123...`)

---

## ⚡ 3-Step Setup

### 1️⃣ Open Config File

File location: `Flask Deployed App/config_oauth.py`

### 2️⃣ Paste Your Credentials

Find these lines and replace with YOUR credentials:

```python
# BEFORE (default):
GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"

# AFTER (your actual credentials):
GOOGLE_CLIENT_ID = "123456789-abc123def456.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-ABC123def456ghi789"
```

**💾 SAVE THE FILE!**

### 3️⃣ Run the App

```powershell
cd "c:\Users\DELL\OneDrive\Desktop\Plant-Disease-Detection-main - Copy\Flask Deployed App"
python app.py
```

---

## ✅ Success Check

Look for this message in the console:
```
✅ Google OAuth credentials loaded from config_oauth.py
```

If you see it → **You're done!** 🎉

---

## 🧪 Test It Now

1. Open: http://127.0.0.1:5000/login
2. Click: "Continue with Google"
3. Sign in with your Google account
4. You should be logged in! ✨

---

## 🔧 If Something's Wrong

### Message: "⚠️ Using default credentials..."

**Problem:** You didn't edit the config file or didn't save it.

**Fix:**
1. Open `config_oauth.py`
2. Make sure you pasted YOUR credentials
3. Save the file (Ctrl+S)
4. Restart the app

---

### Button does nothing

**Fix:** Check Flask console for errors. Make sure you added the correct redirect URI in Google Console:
```
http://127.0.0.1:5000/google-authorize
```

---

## 📁 File You Need to Edit

**ONE FILE only:**
```
Flask Deployed App/
└── config_oauth.py  ← Edit this file!
```

That's it! No environment variables, no complicated setup! 🎉

---

## 🎨 What It Looks Like

**Your Login Page:**
```
┌─────────────────────────────┐
│  [G] Continue with Google   │  ← This button works now!
│                             │
│          OR                 │
│                             │
│  [Username]                 │
│  [Password]                 │
│  [Login]                    │
└─────────────────────────────┘
```

---

## 🔐 Security Tip

Don't share your `config_oauth.py` file with anyone!
It contains your secret credentials.

---

**That's all you need!** 🚀

No environment variables ❌
No complex setup ❌
Just edit one file ✅
