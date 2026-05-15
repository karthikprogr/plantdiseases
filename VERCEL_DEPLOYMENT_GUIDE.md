# ⚡ VERCEL DEPLOYMENT GUIDE - Frontend (React)

**Platform**: Vercel  
**Time Required**: 15-20 minutes  
**Cost**: FREE (generous limits)

---

## ✅ PREREQUISITES

Before starting, ensure you have:
- [ ] Backend deployed to Render.com (get API URL)
- [ ] Firebase Console setup completed
- [ ] GitHub repository with your code
- [ ] Node.js and npm installed locally (for testing)

---

## 📋 STEP-BY-STEP DEPLOYMENT

### STEP 1: PREPARE FRONTEND FOR DEPLOYMENT

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies** (if not already):
   ```bash
   npm install
   ```

3. **Install Firebase SDK:**
   ```bash
   npm install firebase
   ```

4. **Create/update `.gitignore` in frontend folder:**
   ```gitignore
   # Dependencies
   node_modules/
   
   # Production build
   build/
   
   # Environment variables
   .env
   .env.local
   .env.production.local
   .env.development.local
   
   # Logs
   npm-debug.log*
   yarn-debug.log*
   yarn-error.log*
   
   # OS files
   .DS_Store
   Thumbs.db
   ```

5. **Test build locally:**
   ```bash
   npm run build
   ```
   - Should complete without errors
   - Creates `build/` folder with optimized files

---

### STEP 2: UPDATE PACKAGE.JSON (OPTIONAL)

Verify your `package.json` has these scripts:

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

**Note**: Remove the `BUILD_PATH` if it's pointing to Flask static folder:
```json
"build": "BUILD_PATH='../Flask Deployed App/static/build' react-scripts build"
```

Should be:
```json
"build": "react-scripts build"
```

---

### STEP 3: PUSH CODE TO GITHUB

1. **Ensure changes are committed:**
   ```bash
   git add .
   git commit -m "Prepare frontend for Vercel deployment"
   git push origin main
   ```

2. **Verify files on GitHub:**
   - `frontend/package.json`
   - `frontend/src/firebase.js`
   - `frontend/src/services/api.js`
   - `frontend/.env.example`

---

### STEP 4: CREATE VERCEL ACCOUNT

1. **Sign up at Vercel:**
   - Go to https://vercel.com/
   - Click "Sign Up"
   - Choose "Continue with GitHub" (recommended)
   - Authorize Vercel to access your GitHub account

2. **Complete profile setup** if prompted

---

### STEP 5: IMPORT PROJECT

1. **From Vercel Dashboard:**
   - Click "Add New..." → "Project"
   - You'll see list of your GitHub repositories

2. **Import your repository:**
   - Find `plant-disease-detection` repository
   - Click "Import"

3. **Configure Project:**

   **Project Settings:**
   - **Project Name**: `plant-disease-detection` (or your choice)
   - **Framework Preset**: Create React App (auto-detected)
   - **Root Directory**: `frontend` (⚠️ IMPORTANT!)
     - Click "Edit" next to Root Directory
     - Select `frontend` from dropdown
   
   **Build Settings:**
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `build` (auto-filled)
   - **Install Command**: `npm install` (auto-filled)

4. **DO NOT deploy yet!** First add environment variables.

---

### STEP 6: ADD ENVIRONMENT VARIABLES

**CRITICAL**: Click on "Environment Variables" section BEFORE deploying!

Add these variables (click "Add" for each):

```env
# Backend API URL (Use your Render.com URL)
REACT_APP_API_URL=https://your-backend-app.onrender.com

# Firebase Configuration (from Firebase Console)
REACT_APP_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789012
REACT_APP_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

**For each variable:**
1. Click "Add" button
2. Enter **Name** (e.g., `REACT_APP_API_URL`)
3. Enter **Value** (e.g., `https://your-app.onrender.com`)
4. Select **Environment**: Check "Production", "Preview", and "Development"
5. Click "Add"

**Where to get Firebase values:**
1. Go to Firebase Console: https://console.firebase.google.com/
2. Select your project
3. Click gear icon ⚙️ → "Project settings"
4. Scroll to "Your apps" → Web app
5. Copy each value from `firebaseConfig` object

---

### STEP 7: DEPLOY!

1. **Click "Deploy" button**

2. **Watch the build process** (2-3 minutes):
   - Installing dependencies
   - Building React app
   - Optimizing assets
   - Deploying to CDN

3. **Deployment successful** when you see:
   ```
   ✓ Build completed
   ✓ Deployment completed
   🎉 Your project is live!
   ```

4. **Get your URL:**
   ```
   https://plant-disease-detection.vercel.app
   ```
   or
   ```
   https://your-project-name-username.vercel.app
   ```

---

### STEP 8: TEST YOUR DEPLOYMENT

1. **Open your Vercel URL** in browser

2. **Test key features:**
   - [ ] Home page loads
   - [ ] Navigation works
   - [ ] Sign up/Login page accessible
   - [ ] Can see Firebase integration (Google Sign-In button)

3. **Check browser console** (F12):
   - No critical errors
   - API calls go to correct backend URL
   - Firebase initializes properly

---

### STEP 9: UPDATE FIREBASE AUTHORIZED DOMAINS

1. **Go to Firebase Console:**
   - Navigate to Authentication → Settings → Authorized domains

2. **Add Vercel domain:**
   - Click "Add domain"
   - Enter: `your-project.vercel.app`
   - Click "Add"

3. **Also add Vercel preview domains** (for testing):
   - `your-project-git-main-username.vercel.app`
   - `*.vercel.app` (wildcard for all preview deployments)

---

### STEP 10: UPDATE BACKEND CORS

1. **Go to Render Dashboard** (your backend)

2. **Update environment variables:**
   - Find `CORS_ORIGINS` variable
   - Update value:
     ```
     https://your-frontend.vercel.app,https://your-backend.onrender.com
     ```
   - Save changes

3. **Backend will auto-redeploy** (1-2 minutes)

---

### STEP 11: FINAL END-TO-END TEST

1. **Open your Vercel URL**

2. **Test complete flow:**
   - [ ] Sign up with email/password
   - [ ] Or sign in with Google
   - [ ] Upload a plant image
   - [ ] Get prediction result
   - [ ] Check history page
   - [ ] Verify data saves to Firestore

3. **Verify in Firebase Console:**
   - Go to Firestore Database
   - Check `users` collection
   - Check `predictions` collection
   - Confirm data appears

---

## 🎨 CUSTOM DOMAIN (OPTIONAL)

### Add Your Own Domain:

1. **Buy a domain** (Namecheap, GoDaddy, Google Domains, etc.)

2. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Add"
   - Enter your domain: `plantdisease.com`
   - Follow DNS configuration instructions

3. **Update DNS records** (at your domain provider):
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

4. **Wait for DNS propagation** (5 minutes - 48 hours)

5. **Update Firebase authorized domains** with your custom domain

---

## 🐛 TROUBLESHOOTING

### Build Fails: "Module not found: 'firebase'"
**Solution**: 
- Run `npm install firebase` locally
- Commit `package.json` and `package-lock.json`
- Redeploy

### Runtime Error: "Firebase config missing"
**Solution**: 
- Verify all `REACT_APP_FIREBASE_*` variables are set
- Must start with `REACT_APP_` prefix
- Redeploy after adding variables

### API calls fail with CORS error
**Solution**: 
- Update backend `CORS_ORIGINS` to include Vercel URL
- Ensure backend has Flask-CORS enabled
- Check browser console for exact error

### Environment variables not working
**Solution**: 
- Variables must start with `REACT_APP_`
- Must be set BEFORE deployment (or redeploy after adding)
- Check Vercel Dashboard → Settings → Environment Variables

### Page not found (404) on refresh
**Solution**: 
- Vercel handles this automatically for Create React App
- If using custom routing, may need `vercel.json`:
  ```json
  {
    "routes": [
      { "src": "/[^.]+", "dest": "/", "status": 200 }
    ]
  }
  ```

### Blank page after deployment
**Solution**: 
- Check browser console for errors
- Verify `package.json` has correct homepage (or remove it)
- Check build logs for errors
- Ensure all dependencies are in `package.json`

---

## 🔄 UPDATING YOUR DEPLOYMENT

### Automatic Deployments (Recommended):
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Vercel auto-deploys within 30 seconds
4. Get notification when ready

### Manual Redeploy:
1. Go to Vercel Dashboard
2. Click "Deployments" tab
3. Click "..." menu on latest deployment
4. Click "Redeploy"

### Preview Deployments:
- Every pull request gets a preview URL
- Test changes before merging to main
- Auto-deleted after PR is merged

---

## 📊 MONITORING & ANALYTICS

### View Deployment Logs:
1. Go to Vercel Dashboard
2. Click "Deployments"
3. Click on specific deployment
4. See build logs and runtime logs

### Performance Metrics:
1. Click "Analytics" tab (may require Pro plan)
2. See page load times
3. Monitor Web Vitals (Core Web Vitals)

### Error Tracking:
- Integrate with Sentry: https://sentry.io/
- Or use Vercel Analytics (paid)

---

## 💰 FREE TIER LIMITS

| Resource | Limit |
|----------|-------|
| Bandwidth | 100 GB/month |
| Builds | 6000 minutes/month |
| Deployments | Unlimited |
| Team Members | 1 (Hobby plan) |
| Domains | Unlimited |
| Preview Deployments | Unlimited |
| Storage | 100 GB |

**Exceeding limits**: Upgrade to Pro ($20/month) or optimize usage.

---

## ⚡ PERFORMANCE OPTIMIZATION

### Reduce Build Time:
1. Use npm cache:
   ```json
   "scripts": {
     "build": "CI=false react-scripts build"
   }
   ```

2. Minimize dependencies:
   - Remove unused packages
   - Use tree-shaking

### Improve Load Time:
1. Enable code splitting
2. Lazy load components:
   ```javascript
   const LazyComponent = React.lazy(() => import('./Component'));
   ```
3. Optimize images (use WebP)
4. Enable Vercel's image optimization

### SEO Optimization:
1. Add meta tags in `public/index.html`
2. Use React Helmet for dynamic meta
3. Create `robots.txt` and `sitemap.xml`

---

## 🎉 SUCCESS CHECKLIST

- [ ] Frontend deployed to Vercel
- [ ] Can access: `https://your-app.vercel.app`
- [ ] Environment variables configured
- [ ] Firebase authentication works
- [ ] Can connect to backend API
- [ ] Predictions work end-to-end
- [ ] Data saves to Firestore
- [ ] CORS configured correctly
- [ ] Firebase domains updated

---

## 🔗 USEFUL LINKS

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Docs: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- Status Page: https://www.vercel-status.com/

---

## 📞 NEXT STEPS

1. ✅ Save your frontend URL: `https://your-app.vercel.app`
2. ✅ Test complete user journey
3. ✅ Share with friends for beta testing
4. ✅ Review DEPLOYMENT_CHECKLIST.md for final steps

---

**🎊 Congratulations! Your frontend is now live!**

**Your app is fully deployed:**
- 🔥 Frontend: `https://your-app.vercel.app`
- ⚙️ Backend: `https://your-api.onrender.com`
- 🗄️ Database: Firebase Firestore

**Share your app with the world! 🌍**
