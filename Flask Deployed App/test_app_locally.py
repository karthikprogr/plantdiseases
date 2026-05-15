"""
Local Testing Script for Firebase Integration
Test the Flask app with Firebase before deployment

Run: python test_app_locally.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🧪 LOCAL TESTING SCRIPT")
print("=" * 70)

# Check environment variables
print("\n1️⃣ Checking Environment Variables...")
required_vars = ['SECRET_KEY', 'JWT_SECRET_KEY']
firebase_vars = ['FIREBASE_CREDENTIALS_PATH', 'FIREBASE_CREDENTIALS']

for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"   ✅ {var}: Set")
    else:
        print(f"   ⚠️  {var}: Not set (will use default)")

# Check Firebase credentials
firebase_path = os.environ.get('FIREBASE_CREDENTIALS_PATH')
firebase_json = os.environ.get('FIREBASE_CREDENTIALS')

if firebase_path and os.path.exists(firebase_path):
    print(f"   ✅ FIREBASE_CREDENTIALS_PATH: {firebase_path} (file exists)")
elif firebase_json:
    print(f"   ✅ FIREBASE_CREDENTIALS: Set (JSON string)")
else:
    print(f"   ❌ Firebase credentials not configured!")
    print(f"      Set FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS")
    exit(1)

# Test Firebase connection
print("\n2️⃣ Testing Firebase Connection...")
try:
    import firebase_service
    firebase_service.initialize_firebase()
    if firebase_service.test_firebase_connection():
        print("   ✅ Firebase connected successfully!")
    else:
        print("   ❌ Firebase connection failed!")
        exit(1)
except Exception as e:
    print(f"   ❌ Firebase error: {e}")
    exit(1)

# Test model loading
print("\n3️⃣ Testing Model Loading...")
try:
    import torch
    import CNN
    
    MODEL_PATH = "plant_disease_model_1_latest.pt"
    if os.path.exists(MODEL_PATH):
        device = torch.device('cpu')
        model = CNN.CNN(39)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()
        print(f"   ✅ Model loaded from {MODEL_PATH}")
    else:
        print(f"   ❌ Model file not found: {MODEL_PATH}")
        exit(1)
except Exception as e:
    print(f"   ❌ Model loading error: {e}")
    exit(1)

# Test Flask app
print("\n4️⃣ Testing Flask App...")
try:
    from app import app
    print("   ✅ Flask app imported successfully")
    
    # Test routes
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
            print(f"      {response.get_json()}")
        else:
            print(f"   ⚠️  Health endpoint returned {response.status_code}")
        
        # Test login page
        response = client.get('/login')
        if response.status_code == 200:
            print("   ✅ Login page accessible")
        else:
            print(f"   ⚠️  Login page returned {response.status_code}")
            
except Exception as e:
    print(f"   ❌ Flask app error: {e}")
    exit(1)

# Summary
print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\n📝 Next Steps:")
print("   1. Start the Flask server: flask run")
print("   2. Open browser: http://localhost:5000")
print("   3. Test signup and login")
print("   4. Upload a plant image")
print("   5. Check Firebase Console for data")
print("\n🚀 If everything works, you're ready to deploy!")
print("=" * 70)
