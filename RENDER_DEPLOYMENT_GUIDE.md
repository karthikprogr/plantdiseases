# 🚀 RENDER.COM DEPLOYMENT GUIDE - Backend (Flask + PyTorch)

**Platform**: Render.com  
**Time Required**: 30-45 minutes  
**Cost**: FREE (with limitations)

---

## ✅ PREREQUISITES

Before starting, ensure you have:
- [ ] Completed Firebase Console setup (see FIREBASE_SETUP_GUIDE.md)
- [ ] Firebase service account JSON file downloaded
- [ ] GitHub account created
- [ ] Code pushed to GitHub repository (public or private)
- [ ] All environment variables noted down

---

## 📋 STEP-BY-STEP DEPLOYMENT

### STEP 1: PREPARE YOUR CODE FOR DEPLOYMENT

1. **Ensure all files are ready:**
   ```
   Flask Deployed App/
   ├── app.py
   ├── firebase_service.py
   ├── CNN.py
   ├── requirements-production.txt
   ├── Procfile
   ├── plant_disease_model_1_latest.pt
   ├── disease_info.csv
   ├── supplement_info.csv
   ├── .gitignore
   └── .env.example
   ```

2. **Verify .gitignore includes:**
   ```gitignore
   .env
   firebase-credentials.json
   *.csv (if you want to exclude user data)
   __pycache__/
   ```

3. **Test locally** (optional but recommended):
   ```bash
   cd "Flask Deployed App"
   pip install -r requirements-production.txt
   python -c "import firebase_service; firebase_service.test_firebase_connection()"
   ```

---

### STEP 2: PUSH CODE TO GITHUB

1. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Prepare for deployment"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Name: `plant-disease-detection`
   - Description: "Plant disease detection app with PyTorch and Firebase"
   - Public or Private: Your choice (Render supports both)
   - Don't initialize with README (you already have one)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/plant-disease-detection.git
   git branch -M main
   git push -u origin main
   ```

---

### STEP 3: CREATE RENDER.COM ACCOUNT

1. **Sign up at Render.com:**
   - Go to https://render.com/
   - Click "Get Started" or "Sign Up"
   - Choose "Sign up with GitHub" (recommended for easy integration)
   - Authorize Render to access your GitHub account
   - Complete profile setup

2. **Verify email** if prompted

---

### STEP 4: CREATE WEB SERVICE

1. **Navigate to Dashboard:**
   - After login, click "New +" button (top right)
   - Select "Web Service"

2. **Connect Repository:**
   - You'll see list of your GitHub repositories
   - Find and click "Connect" next to `plant-disease-detection`
   - If not visible, click "Configure account" to grant access

3. **Configure Service:**

   **Basic Settings:**
   - **Name**: `plant-disease-api` (or your choice)
   - **Region**: Choose closest to you (Oregon, Frankfurt, Singapore, Ohio)
   - **Branch**: `main`
   - **Root Directory**: `Flask Deployed App` (important!)
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements-production.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn app:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
     ```

   **Instance Type:**
   - Select **"Free"**
   - 512 MB RAM, 0.1 CPU
   - Sleeps after 15 min inactivity
   - Auto-wakes on request (30-60s cold start)

4. **Click "Advanced"** to expand additional settings:
   - **Auto-Deploy**: Yes (recommended)
   - **Health Check Path**: `/` or `/health` (if you create health endpoint)

---

### STEP 5: ADD ENVIRONMENT VARIABLES

**CRITICAL**: Add these environment variables before deploying!

Click "Add Environment Variable" for each:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=<click "Generate" button to create random key>
JWT_SECRET_KEY=<click "Generate" button to create another key>
PYTHON_VERSION=3.10.12

# Firebase Configuration
FIREBASE_CREDENTIALS=<paste ENTIRE JSON from service account file>

# OpenAI (Optional)
OPENAI_API_KEY=<your-openai-api-key>

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=<your-email@gmail.com>
MAIL_PASSWORD=<your-app-specific-password>

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=<your-client-id>.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=<your-client-secret>

# CORS (Add your frontend URL after Vercel deployment)
CORS_ORIGINS=https://your-app.vercel.app

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
```

**For FIREBASE_CREDENTIALS:**
1. Open your downloaded `firebase-service-account.json`
2. Copy the ENTIRE contents (all JSON)
3. Paste into the value field
4. It should look like: `{"type":"service_account","project_id":"...","private_key":"-----BEGIN...}`

---

### STEP 6: CREATE PERSISTENT DISK (OPTIONAL)

If you want to store uploaded images persistently:

1. Scroll to **"Disks"** section
2. Click "Add Disk"
3. **Name**: `uploads`
4. **Mount Path**: `/opt/render/project/src/Flask Deployed App/static/uploads`
5. **Size**: 1 GB (free tier maximum)
6. Click "Save"

**Note**: Without disk, uploads will be lost when service restarts.

---

### STEP 7: DEPLOY!

1. Click **"Create Web Service"** button at bottom
2. Wait for deployment (5-10 minutes first time)
3. Watch the logs in real-time:
   - Building dependencies
   - Installing PyTorch (this takes longest)
   - Installing Firebase Admin SDK
   - Starting gunicorn server

4. **Deployment successful** when you see:
   ```
   [INFO] Listening at: http://0.0.0.0:10000
   Your service is live 🎉
   ```

---

### STEP 8: GET YOUR API URL

1. After deployment, you'll see your service URL:
   ```
   https://plant-disease-api.onrender.com
   ```

2. **Test the deployment:**
   - Open: `https://your-app.onrender.com/`
   - You should see your Flask home page or an error (if no route defined)

3. **Test API health** (if you create /health endpoint):
   ```bash
   curl https://your-app.onrender.com/health
   ```

---

### STEP 9: UPDATE FIREBASE AUTHORIZED DOMAINS

1. Go to Firebase Console
2. Navigate to **Authentication** → **Settings** → **Authorized domains**
3. Click "Add domain"
4. Add: `your-app.onrender.com`
5. Click "Add"

---

### STEP 10: UPDATE CORS IN FLASK (AFTER VERCEL DEPLOYMENT)

After you deploy frontend to Vercel:

1. Go to Render Dashboard → Your Service → Environment
2. Find `CORS_ORIGINS` variable
3. Update value:
   ```
   https://your-frontend.vercel.app,https://your-app.onrender.com
   ```
4. Save changes
5. Service will auto-redeploy

---

## 🐛 TROUBLESHOOTING

### Build Fails: "No module named 'firebase_admin'"
**Solution**: Check `requirements-production.txt` includes `firebase-admin==6.2.0`

### Build Fails: PyTorch installation timeout
**Solution**: This is common. Render will retry automatically. Wait or manually trigger retry.

### Runtime Error: "Firebase credentials not found"
**Solution**: 
- Verify `FIREBASE_CREDENTIALS` environment variable is set
- Ensure entire JSON is pasted (no line breaks removed)
- Check logs for specific error message

### Error: "Port already in use"
**Solution**: Make sure your start command uses `$PORT` variable:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Service sleeps after 15 minutes
**Solution**: This is normal for free tier. Service wakes automatically on first request (30-60s delay).

### CORS errors from frontend
**Solution**: 
- Verify `CORS_ORIGINS` includes your frontend URL
- Add `Flask-CORS` to requirements
- Ensure app.py has CORS configured:
  ```python
  from flask_cors import CORS
  CORS(app, origins=os.environ.get('CORS_ORIGINS', '').split(','))
  ```

### Model file too large (>100MB)
**Solution**: 
- Option 1: Use Git LFS (Large File Storage)
- Option 2: Upload model to Google Drive, download on startup:
  ```python
  import gdown
  gdown.download(GOOGLE_DRIVE_URL, MODEL_PATH, quiet=False)
  ```

---

## 📊 MONITORING YOUR DEPLOYMENT

### View Logs:
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time application logs

### View Metrics:
1. Click "Metrics" tab
2. See CPU, Memory, Request rate
3. Monitor for performance issues

### Set up Notifications:
1. Go to "Settings" → "Notifications"
2. Add email or Slack webhook
3. Get alerted on deploy failures

---

## 🔄 UPDATING YOUR DEPLOYMENT

### Automatic Updates (Recommended):
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature X"
   git push origin main
   ```
3. Render auto-deploys within 1-2 minutes
4. Watch logs to confirm successful deployment

### Manual Deploy:
1. Go to Render Dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 💰 FREE TIER LIMITATIONS

| Resource | Limit |
|----------|-------|
| RAM | 512 MB |
| CPU | 0.1 CPU share |
| Bandwidth | 100 GB/month |
| Build Time | 15 minutes |
| Disk | 1 GB (persistent disk) |
| Sleep | After 15 min inactivity |
| Cold Start | 30-60 seconds |
| Services | Unlimited |

**Exceeding limits**: Service will be throttled or temporarily suspended.

---

## ⚡ PERFORMANCE OPTIMIZATION

### Reduce Cold Start Time:
1. Keep model file small (<50MB if possible)
2. Use lazy loading for heavy imports
3. Implement health check endpoint

### Improve Response Time:
1. Use CDN for static files
2. Implement caching (Redis - paid tier)
3. Optimize model inference

### Prevent Sleep:
- Use free services like UptimeRobot to ping every 14 minutes
- URL: https://uptimerobot.com/

---

## 🎉 SUCCESS CHECKLIST

- [ ] Service deployed successfully
- [ ] Can access: `https://your-app.onrender.com/`
- [ ] Firebase connection working
- [ ] Model loads without errors
- [ ] Can make prediction requests
- [ ] Logs show no critical errors
- [ ] Domain added to Firebase authorized domains

---

## 🔗 USEFUL LINKS

- Render Dashboard: https://dashboard.render.com/
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com/
- Status Page: https://status.render.com/

---

## 📞 NEXT STEPS

1. ✅ Save your API URL: `https://your-app.onrender.com`
2. ✅ Test all endpoints with Postman or curl
3. ✅ Proceed to VERCEL_DEPLOYMENT_GUIDE.md for frontend deployment
4. ✅ Update frontend API URL with your Render URL

---

**🎊 Congratulations! Your backend is now live!**
