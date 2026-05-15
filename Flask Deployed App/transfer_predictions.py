"""
Transfer all predictions to the currently logged-in user
This will help if you have multiple accounts and predictions are scattered
"""
from app import app, db
from models import User, Prediction

with app.app_context():
    print("\n🔄 PREDICTION TRANSFER TOOL\n" + "="*60)
    
    # Show all users and their prediction counts
    users = User.query.all()
    print(f"\n📊 Current Status:")
    print("-" * 60)
    for i, user in enumerate(users, 1):
        count = Prediction.query.filter_by(user_id=user.id).count()
        print(f"{i}. User ID {user.id}: {user.username}")
        print(f"   Predictions: {count}")
        print()
    
    # Ask which user to transfer FROM and TO
    print("\n" + "="*60)
    from_user_id = input("Enter the User ID who HAS predictions (from above): ").strip()
    to_user_id = input("Enter the User ID who SHOULD HAVE predictions: ").strip()
    
    try:
        from_user_id = int(from_user_id)
        to_user_id = int(to_user_id)
        
        # Verify users exist
        from_user = User.query.get(from_user_id)
        to_user = User.query.get(to_user_id)
        
        if not from_user or not to_user:
            print("❌ Invalid user ID(s)")
            exit()
        
        # Count predictions to transfer
        predictions = Prediction.query.filter_by(user_id=from_user_id).all()
        count = len(predictions)
        
        if count == 0:
            print(f"❌ User {from_user.username} has no predictions to transfer")
            exit()
        
        print(f"\n⚠️  About to transfer {count} predictions:")
        print(f"   FROM: {from_user.username} (ID: {from_user_id})")
        print(f"   TO:   {to_user.username} (ID: {to_user_id})")
        
        confirm = input(f"\nType 'YES' to confirm: ").strip()
        
        if confirm == 'YES':
            for pred in predictions:
                pred.user_id = to_user_id
            
            db.session.commit()
            print(f"\n✅ Successfully transferred {count} predictions!")
            print(f"   {to_user.username} now has all predictions.")
            
            # Verify
            new_count = Prediction.query.filter_by(user_id=to_user_id).count()
            print(f"\n📊 Verification: User {to_user.username} now has {new_count} predictions")
        else:
            print("❌ Transfer cancelled")
    
    except ValueError:
        print("❌ Please enter valid numbers")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()
    
    print("\n" + "="*60 + "\n")
