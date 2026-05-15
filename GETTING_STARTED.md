# 🚀 GETTING STARTED - LOCAL DEVELOPMENT

**Follow these steps to run your app locally with Firebase**

---

## ✅ STEP 1: Install Dependencies

```bash
cd "Flask Deployed App"
pip install -r requirements-production.txt
```

**What this installs:**
- Flask and related packages
- PyTorch (CPU version)
- Firebase Admin SDK
- All other dependencies

---

## ✅ STEP 2: Setup Firebase Credentials

### Option A: Use JSON File (Recommended for Local Development)

1. **Download your Firebase service account JSON** from Firebase Console:
   - Go to: https://console.firebase.google.com/
   - Select your project
   - Settings → Service Accounts
   - Click "Generate new private key"
   - Save as `firebase-credentials.json` in `Flask Deployed App` folder

2. **Create `.env` file** in `Flask Deployed App`:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json

# Optional: OpenAI (for chatbot)
OPENAI_API_KEY=your-openai-key

# Optional: Email (for password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

---

## ✅ STEP 3: Test Firebase Connection

```bash
python test_app_locally.py
```

**Expected output:**
```
🧪 LOCAL TESTING SCRIPT
======================================================================
1️⃣ Checking Environment Variables...
   ✅ SECRET_KEY: Set
   ✅ JWT_SECRET_KEY: Set
   ✅ FIREBASE_CREDENTIALS_PATH: firebase-credentials.json (file exists)

2️⃣ Testing Firebase Connection...
   ✅ Firebase connected successfully!

3️⃣ Testing Model Loading...
   ✅ Model loaded from plant_disease_model_1_latest.pt

4️⃣ Testing Flask App...
   ✅ Flask app imported successfully
   ✅ Health endpoint working
   ✅ Login page accessible

======================================================================
✅ ALL TESTS PASSED!
======================================================================
```

---

## ✅ STEP 4: Run the Flask App

```bash
flask run
```

Or:

```bash
python app.py
```

**App will start on:** http://localhost:5000

---

## ✅ STEP 5: Test the Application

### Test 1: Health Check
Open: http://localhost:5000/health

Should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-13T...",
  "firebase": "connected",
  "model": "loaded"
}
```

### Test 2: Sign Up
1. Go to: http://localhost:5000/signup
2. Enter email and password
3. Check Firebase Console → Firestore → users collection
4. You should see your new user

### Test 3: Login
1. Go to: http://localhost:5000/login
2. Login with your credentials
3. Should redirect to home page

### Test 4: Upload Image
1. Click "Disease Recognition"
2. Upload a plant leaf image
3. Get prediction result
4. Check Firebase Console → Firestore → predictions collection
5. Your prediction should be saved

### Test 5: View History
1. Click "My History"
2. Should see your predictions
3. Data is coming from Firebase Firestore

---

## 🐛 TROUBLESHOOTING

### Error: "Firebase credentials not found"
**Solution:**
- Make sure `firebase-credentials.json` exists in `Flask Deployed App` folder
- Check `.env` file has `FIREBASE_CREDENTIALS_PATH=firebase-credentials.json`
- Verify the JSON file is not corrupted

### Error: "Model not loaded"
**Solution:**
- Make sure `plant_disease_model_1_latest.pt` exists
- File should be in `Flask Deployed App` folder
- Check file is not corrupted (should be ~80-100MB)

### Error: "ModuleNotFoundError"
**Solution:**
- Run: `pip install -r requirements-production.txt`
- Make sure you're in the correct virtual environment

### Error: "Permission denied"
**Solution:**
- Run command prompt as administrator
- Or use: `python -m flask run`

### Port Already in Use
**Solution:**
- Close other Flask instances
- Or use different port: `flask run --port 5001`

---

## 📱 FRONTEND SETUP (Optional for Local Testing)

If you want to test the React frontend locally:

```bash
cd frontend
npm install
npm start
```

Frontend will start on: http://localhost:3000

---

## ✨ FEATURES TO TEST

- [x] Sign up with email/password
- [x] Login
- [x] Upload plant image
- [x] Get disease prediction
- [x] View confidence score
- [x] See recommendations
- [x] View prediction history
- [x] Data saves to Firebase Firestore

---

## 🔍 VERIFY FIREBASE DATA

After testing, check Firebase Console:

1. **Go to Firebase Console:** https://console.firebase.google.com/
2. **Select your project**
3. **Firestore Database:**
   - Click "users" collection → See your user
   - Click "predictions" collection → See your predictions

---

## 📊 MONITORING

### View Logs:
- Flask logs in terminal
- Firebase operations show ✅ or ❌ indicators

### Check Health:
```bash
curl http://localhost:5000/health
```

---

## 🎯 NEXT STEPS

Once everything works locally:

1. ✅ Your app runs without errors
2. ✅ Firebase connection works
3. ✅ Data saves to Firestore
4. ✅ Predictions work correctly

**You're ready to deploy!**

Follow the deployment guides:
- [RENDER_DEPLOYMENT_GUIDE.md](../RENDER_DEPLOYMENT_GUIDE.md) - Backend
- [VERCEL_DEPLOYMENT_GUIDE.md](../VERCEL_DEPLOYMENT_GUIDE.md) - Frontend

---

## 🆘 NEED HELP?

### Check These Files:
- `test_app_locally.py` - Run comprehensive tests
- `firebase_service.py` - Firebase operations
- `app.py` - Main Flask application

### Common Issues:
1. **Firebase not connecting** → Check credentials
2. **Model not loading** → Check file exists
3. **CORS errors** → Update CORS_ORIGINS in .env

---

**🎉 Happy Coding! Your plant disease detection app is ready to run!**
