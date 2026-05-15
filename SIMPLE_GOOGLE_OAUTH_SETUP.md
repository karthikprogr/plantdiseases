# 🎯 Simple Google OAuth Setup - No Environment Variables Needed!

## ✨ Super Easy Setup (3 Steps)

### Step 1: Get Your Google Credentials (2 minutes)

1. Go to: https://console.cloud.google.com/apis/credentials
2. You should see your newly created OAuth client
3. Click on it to see your credentials
4. **Copy** the Client ID
5. **Copy** the Client Secret

---

### Step 2: Edit the Config File (1 minute)

1. Open this file: `Flask Deployed App/config_oauth.py`
2. Find these lines:
   ```python
   GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
   ```

3. Replace with YOUR actual credentials:
   ```python
   GOOGLE_CLIENT_ID = "123456789-abc123.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET = "GOCSPX-abc123def456"
   ```

4. **Save the file**

---

### Step 3: Run Your App (30 seconds)

```powershell
cd "c:\Users\DELL\OneDrive\Desktop\Plant-Disease-Detection-main - Copy\Flask Deployed App"
python app.py
```

That's it! 🎉

---

## 🧪 Test It

1. Open browser: http://127.0.0.1:5000/login
2. Click "Continue with Google"
3. Sign in with your Google account
4. Done! You should be logged in! ✅

---

## 📝 What Changed?

**Before (complicated):**
- Set environment variables
- Different for each terminal
- Hard to remember
- Variables lost when terminal closes

**Now (simple):**
- Edit one file: `config_oauth.py`
- Paste your credentials
- Save and run
- Works every time! ✨

---

## 🔧 Troubleshooting

### Issue: "YOUR_CLIENT_ID_HERE" in console

**Fix:** You forgot to edit `config_oauth.py`. Open it and paste your real credentials.

### Issue: "ModuleNotFoundError: No module named 'config_oauth'"

**Fix:** Make sure `config_oauth.py` is in the `Flask Deployed App` folder.

### Issue: Still getting errors

**Fix:** Make sure you:
1. Saved the config file after editing
2. Pasted the complete Client ID (including .apps.googleusercontent.com)
3. Pasted the complete Client Secret (starts with GOCSPX-)

---

## 📁 File Structure

```
Flask Deployed App/
├── app.py                    (updated to read from config)
├── config_oauth.py          (NEW - your credentials go here!)
├── models.py
├── CNN.py
└── templates/
    ├── login.html           (has Google button)
    └── signup.html          (has Google button)
```

---

## ✅ Quick Checklist

- [ ] Created OAuth client in Google Console
- [ ] Copied Client ID
- [ ] Copied Client Secret
- [ ] Opened `config_oauth.py`
- [ ] Pasted Client ID (line 18)
- [ ] Pasted Client Secret (line 21)
- [ ] Saved the file
- [ ] Ran `python app.py`
- [ ] Tested login with Google
- [ ] Successfully logged in! 🎉

---

## 🎨 Visual Guide

### Before (Complex Setup):
```
Terminal 1: $env:GOOGLE_CLIENT_ID="..."
Terminal 2: $env:GOOGLE_CLIENT_ID="..." (forgot to set!)
Terminal 3: $env:GOOGLE_CLIENT_ID="..." (typo!)
❌ Confusing and error-prone
```

### After (Simple Setup):
```
config_oauth.py
├─ GOOGLE_CLIENT_ID = "your-id"
├─ GOOGLE_CLIENT_SECRET = "your-secret"
└─ Save file → Works everywhere! ✅
```

---

## 🔐 Security Note

⚠️ **Important:** Add `config_oauth.py` to `.gitignore` so you don't accidentally commit your credentials to Git!

Create/edit `.gitignore` file:
```
config_oauth.py
*.pyc
__pycache__/
instance/
.env
```

---

## 💡 Pro Tip

Keep a backup of your credentials in a safe place (like a password manager) in case you need them later!

---

## 🎉 That's It!

No more:
- ❌ Environment variables
- ❌ PowerShell commands
- ❌ Lost credentials
- ❌ Terminal-specific setup

Just:
- ✅ Edit one file
- ✅ Save
- ✅ Run
- ✅ Works!

**Enjoy your Google Sign-In!** 🚀

---

## 📞 Need Help?

If the app shows:
```
✅ Google OAuth credentials loaded from config_oauth.py
```

You're good to go! If you see:
```
⚠️ Using default credentials. Edit config_oauth.py...
```

Then you need to add your credentials to the config file.

Happy coding! 🌱✨
