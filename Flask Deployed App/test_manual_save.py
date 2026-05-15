"""
Manual test to add a prediction directly to database
This will help us verify if the database saving works at all
"""
from app import app, db
from models import User, Prediction
from datetime import datetime

with app.app_context():
    print("\n🧪 MANUAL PREDICTION TEST\n" + "="*50)
    
    # Get first user
    user = User.query.first()
    if not user:
        print("❌ No users found! Create a user first.")
        exit()
    
    print(f"✅ Found user: {user.username} (ID: {user.id})")
    
    # Create a test prediction
    test_prediction = Prediction(
        user_id=user.id,
        image_path='uploads/test_image.jpg',
        original_filename='test_image.jpg',
        predicted_class=1,
        disease_name='Apple___Black_rot',
        confidence=0.95,
        is_valid_plant=True,
        ip_address='127.0.0.1',
        user_agent='Manual Test'
    )
    
    try:
        db.session.add(test_prediction)
        db.session.commit()
        print(f"✅ Test prediction saved with ID: {test_prediction.id}")
        
        # Verify it was saved
        saved = Prediction.query.get(test_prediction.id)
        print(f"✅ Verification: {saved.disease_name} at {saved.timestamp}")
        
        # Count predictions for this user
        count = Prediction.query.filter_by(user_id=user.id).count()
        print(f"✅ Total predictions for {user.username}: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()
    
    print("="*50 + "\n")
