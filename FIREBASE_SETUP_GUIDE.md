# 🔥 FIREBASE CONSOLE SETUP GUIDE

**Complete this setup BEFORE deployment. Time: 20 minutes**

---

## STEP 1: CREATE FIREBASE PROJECT

1. **Go to Firebase Console:**
   - Open: https://console.firebase.google.com/
   - Click **"Add project"** or **"Create a project"**

2. **Configure Project:**
   - **Project name:** `plant-disease-detection` (or your choice)
   - Click **Continue**
   - **Google Analytics:** Toggle OFF (not needed) or keep ON
   - Click **Create project**
   - Wait 30 seconds for setup
   - Click **Continue**

---

## STEP 2: ENABLE FIRESTORE DATABASE

1. **Navigate to Firestore:**
   - In left sidebar, click **"Build"** → **"Firestore Database"**
   - Click **"Create database"**

2. **Configure Firestore:**
   - **Location:** Select `us-central1` (or closest to you)
   - Click **Next**
   - **Security rules:** Select **"Start in production mode"**
     ```
     rules_version = '2';
     service cloud.firestore {
       match /databases/{database}/documents {
         match /{document=**} {
           allow read, write: if request.auth != null;
         }
       }
     }
     ```
   - Click **Enable**
   - Wait for database creation (30 seconds)

3. **Update Security Rules (Important!):**
   - Click **"Rules"** tab
   - Replace with:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Users collection
       match /users/{userId} {
         allow read, write: if request.auth != null && request.auth.uid == userId;
         allow create: if request.auth != null;
       }
       
       // Predictions collection
       match /predictions/{predictionId} {
         allow read, write: if request.auth != null;
       }
       
       // Allow admin access from backend (via service account)
       match /{document=**} {
         allow read, write: if request.auth.token.admin == true;
       }
     }
   }
   ```
   - Click **Publish**

---

## STEP 3: ENABLE AUTHENTICATION

1. **Navigate to Authentication:**
   - In left sidebar, click **"Build"** → **"Authentication"**
   - Click **"Get started"**

2. **Enable Sign-in Methods:**
   
   **A. Enable Email/Password:**
   - Click **"Email/Password"**
   - Toggle **Enable** ON
   - Click **Save**
   
   **B. Enable Google Sign-In:**
   - Click **"Google"**
   - Toggle **Enable** ON
   - **Project support email:** Select your email
   - Click **Save**

3. **Configure Authorized Domains (Do this AFTER deployment):**
   - Click **"Settings"** tab → **"Authorized domains"**
   - By default, `localhost` is authorized
   - **After deployment, add:**
     - Your Vercel domain: `your-app.vercel.app`
     - Your Render domain: `your-app.onrender.com`
   - Click **"Add domain"** for each

---

## STEP 4: CREATE WEB APP & GET CREDENTIALS

1. **Register Web App:**
   - Go to **Project Overview** (home icon in sidebar)
   - Click **gear icon** (⚙️) next to "Project Overview" → **"Project settings"**
   - Scroll down to **"Your apps"** section
   - Click **"</>" (Web)** icon

2. **Configure Web App:**
   - **App nickname:** `plant-disease-web`
   - ✅ Check **"Also set up Firebase Hosting"** → **NO** (uncheck it)
   - Click **"Register app"**

3. **Copy Firebase Config:**
   - You'll see code like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     authDomain: "plant-disease-detection.firebaseapp.com",
     projectId: "plant-disease-detection",
     storageBucket: "plant-disease-detection.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef123456"
   };
   ```
   - **COPY THIS ENTIRE OBJECT** - you'll need it for frontend
   - Click **Continue to console**

---

## STEP 5: GENERATE SERVICE ACCOUNT (FOR BACKEND)

1. **Navigate to Service Accounts:**
   - Click **gear icon** (⚙️) → **"Project settings"**
   - Click **"Service accounts"** tab

2. **Generate Private Key:**
   - Click **"Generate new private key"** button
   - Click **"Generate key"** in popup
   - A JSON file will download: `plant-disease-detection-xxxxxx.json`
   - **SAVE THIS FILE SECURELY** - it's like a password!

3. **JSON File Contents (Example):**
   ```json
   {
     "type": "service_account",
     "project_id": "plant-disease-detection",
     "private_key_id": "abc123...",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "firebase-adminsdk-xxxxx@plant-disease-detection.iam.gserviceaccount.com",
     "client_id": "123456789",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
   }
   ```

---

## STEP 6: ORGANIZE YOUR CREDENTIALS

Create a file **locally** (DON'T commit to Git):

**File: `Firebase Deployed App/firebase-credentials.json`**
- Copy the entire service account JSON here
- Add to `.gitignore`:
  ```
  firebase-credentials.json
  *.json
  ```

**File: `frontend/.env.local`** (Create this):
```env
REACT_APP_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
REACT_APP_FIREBASE_AUTH_DOMAIN=plant-disease-detection.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=plant-disease-detection
REACT_APP_FIREBASE_STORAGE_BUCKET=plant-disease-detection.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789012
REACT_APP_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

---

## STEP 7: TEST FIREBASE CONNECTION (OPTIONAL)

1. **Create Test Document in Firestore:**
   - Go to **Firestore Database**
   - Click **"Start collection"**
   - **Collection ID:** `test`
   - Click **Next**
   - **Document ID:** Auto-ID
   - **Field:** `message`, Type: `string`, Value: `Hello Firebase!`
   - Click **Save**

2. **Verify:**
   - You should see the document in Firestore
   - Delete it after testing

---

## STEP 8: IMPORTANT SECURITY NOTES

### 🔒 NEVER COMMIT THESE FILES TO GIT:
- `firebase-credentials.json` (service account)
- `.env` files with credentials
- Any file with `private_key`

### ✅ ADD TO `.gitignore`:
```gitignore
# Firebase
firebase-credentials.json
serviceAccountKey.json
*-firebase-adminsdk-*.json

# Environment variables
.env
.env.local
.env.production.local
```

### 🔑 FOR DEPLOYMENT:
- **Backend (Render.com):** Paste service account JSON as environment variable
- **Frontend (Vercel):** Add Firebase config values as environment variables

---

## STEP 9: ENABLE FIREBASE STORAGE (OPTIONAL)

**Only if you want to store images in Firebase instead of server:**

1. **Navigate to Storage:**
   - Click **"Build"** → **"Storage"**
   - Click **"Get started"**

2. **Configure:**
   - Click **Next** (default security rules)
   - Select **location:** `us-central1`
   - Click **Done**

3. **Update Rules:**
   ```javascript
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /uploads/{userId}/{allPaths=**} {
         allow read: if request.auth != null;
         allow write: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```

---

## ✅ CHECKLIST - CONFIRM YOU HAVE:

- [ ] Firebase project created
- [ ] Firestore Database enabled with security rules
- [ ] Authentication enabled (Email + Google)
- [ ] Web app registered
- [ ] Firebase config copied (for frontend)
- [ ] Service account JSON downloaded (for backend)
- [ ] Files added to `.gitignore`
- [ ] `.env.local` created in frontend folder

---

## 🎯 NEXT STEPS:

After completing this setup:
1. ✅ Return to main deployment process
2. ✅ Install Firebase SDK in backend and frontend
3. ✅ Migrate CSV data to Firestore
4. ✅ Deploy to Render.com and Vercel

---

## 📞 TROUBLESHOOTING:

**Problem: Can't find "Firestore Database"**
- Solution: Make sure you're in correct project, refresh page

**Problem: Google Sign-In not working**
- Solution: Add authorized domains after deployment

**Problem: Permission denied errors**
- Solution: Check Firestore security rules, ensure auth is enabled

**Problem: Service account JSON not downloading**
- Solution: Check browser downloads, try different browser

---

## 🔗 USEFUL LINKS:

- Firebase Console: https://console.firebase.google.com/
- Firestore Docs: https://firebase.google.com/docs/firestore
- Auth Docs: https://firebase.google.com/docs/auth
- Security Rules: https://firebase.google.com/docs/firestore/security/get-started

---

**🎉 Once complete, you're ready to integrate Firebase with your app!**
