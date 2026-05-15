"""
Quick test script to check if predictions are being saved to database
Run this: python test_database.py
"""
from app import app, db, Prediction, User
from datetime import datetime

with app.app_context():
    print("\n🔍 DATABASE TEST\n" + "="*50)
    
    # Check all users
    users = User.query.all()
    print(f"\n📊 Total Users: {len(users)}")
    for user in users:
        print(f"  - User ID: {user.id}, Username: {user.username}")
    
    # Check all predictions
    predictions = Prediction.query.all()
    print(f"\n📊 Total Predictions: {len(predictions)}")
    for pred in predictions[:10]:  # Show first 10
        print(f"  - ID: {pred.id}, User: {pred.user_id}, Disease: {pred.disease_name}, Confidence: {pred.confidence:.2%}, Date: {pred.timestamp}")
    
    if len(predictions) > 10:
        print(f"  ... and {len(predictions) - 10} more predictions")
    
    # Show predictions per user
    print(f"\n📊 Predictions Per User:")
    for user in users:
        count = Prediction.query.filter_by(user_id=user.id).count()
        print(f"  - {user.username}: {count} predictions")
    
    print("\n" + "="*50 + "\n")
