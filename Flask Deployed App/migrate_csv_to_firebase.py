"""
CSV to Firebase Migration Script
Migrates existing users.csv and predictions.csv to Firestore

Usage: python migrate_csv_to_firebase.py
"""

import os
import csv
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path to import firebase_service
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import firebase_service

# Load environment variables
load_dotenv()

def migrate_users():
    """Migrate users from CSV to Firestore"""
    csv_file = 'users.csv'
    
    if not os.path.exists(csv_file):
        print(f"⚠️  {csv_file} not found - skipping user migration")
        return
    
    print(f"\n📊 Migrating users from {csv_file}...")
    migrated = 0
    errors = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    email = row.get('email', '').strip()
                    full_name = row.get('full_name', '').strip()
                    phone = row.get('phone', '').strip()
                    password = row.get('password', '')  # This is hashed
                    
                    if not email:
                        print(f"⚠️  Skipping row with empty email")
                        continue
                    
                    # Check if user already exists
                    existing_user = firebase_service.get_user_by_email(email)
                    if existing_user:
                        print(f"⚠️  User {email} already exists - skipping")
                        continue
                    
                    # Create user (Note: Firebase requires plain password, not hashed)
                    # You'll need to set a temporary password or ask users to reset
                    temp_password = "TempPass123!"  # Users will need to reset via email
                    
                    result = firebase_service.create_user(
                        email=email,
                        password=temp_password,
                        full_name=full_name,
                        phone=phone
                    )
                    
                    if result['success']:
                        print(f"✅ Migrated user: {email}")
                        migrated += 1
                    else:
                        print(f"❌ Failed to migrate {email}: {result['message']}")
                        errors += 1
                        
                except Exception as e:
                    print(f"❌ Error migrating user: {e}")
                    errors += 1
    
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return
    
    print(f"\n✅ Users Migration Complete:")
    print(f"   - Migrated: {migrated}")
    print(f"   - Errors: {errors}")
    print(f"\n⚠️  IMPORTANT: All users have temporary password 'TempPass123!'")
    print(f"   - Send password reset emails to all users")
    print(f"   - Or implement a password reset flow")


def migrate_predictions():
    """Migrate predictions from CSV to Firestore"""
    csv_file = 'predictions.csv'
    
    if not os.path.exists(csv_file):
        print(f"⚠️  {csv_file} not found - skipping prediction migration")
        return
    
    print(f"\n📊 Migrating predictions from {csv_file}...")
    migrated = 0
    errors = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    user_email = row.get('user_email', '').strip()
                    image_name = row.get('image_name', '').strip()
                    prediction = row.get('prediction', '').strip()
                    confidence = float(row.get('confidence', 0))
                    supplement = row.get('supplement', '').strip()
                    description = row.get('description', '').strip()
                    
                    if not user_email or not prediction:
                        print(f"⚠️  Skipping incomplete prediction")
                        continue
                    
                    # Save to Firestore
                    prediction_id = firebase_service.save_prediction(
                        user_email=user_email,
                        image_name=image_name,
                        prediction=prediction,
                        confidence=confidence,
                        supplement=supplement,
                        description=description
                    )
                    
                    if prediction_id:
                        migrated += 1
                        if migrated % 10 == 0:
                            print(f"   Migrated {migrated} predictions...")
                    else:
                        errors += 1
                        
                except Exception as e:
                    print(f"❌ Error migrating prediction: {e}")
                    errors += 1
    
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return
    
    print(f"\n✅ Predictions Migration Complete:")
    print(f"   - Migrated: {migrated}")
    print(f"   - Errors: {errors}")


def backup_csv_files():
    """Create backups of CSV files before migration"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    files_to_backup = ['users.csv', 'predictions.csv']
    
    print("\n💾 Creating backups of CSV files...")
    
    for file in files_to_backup:
        if os.path.exists(file):
            backup_name = f"{file}.backup_{timestamp}"
            
            try:
                with open(file, 'r', encoding='utf-8') as src:
                    with open(backup_name, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"✅ Backed up {file} → {backup_name}")
            except Exception as e:
                print(f"❌ Failed to backup {file}: {e}")
        else:
            print(f"⚠️  {file} not found - skipping backup")


def main():
    """Main migration function"""
    print("=" * 60)
    print("🔥 CSV to Firebase Migration Tool")
    print("=" * 60)
    
    # Test Firebase connection first
    print("\n🔍 Testing Firebase connection...")
    if not firebase_service.test_firebase_connection():
        print("❌ Firebase connection failed!")
        print("   Make sure:")
        print("   1. Firebase credentials are set in .env")
        print("   2. FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS is configured")
        return
    
    print("✅ Firebase connection successful!")
    
    # Confirm before proceeding
    print("\n⚠️  This will migrate data from CSV files to Firestore")
    print("   - users.csv → Firestore users collection")
    print("   - predictions.csv → Firestore predictions collection")
    
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Migration cancelled")
        return
    
    # Create backups
    backup_csv_files()
    
    # Migrate data
    migrate_users()
    migrate_predictions()
    
    # Show statistics
    print("\n" + "=" * 60)
    print("📊 Migration Summary")
    print("=" * 60)
    
    stats = firebase_service.get_prediction_stats()
    print(f"Total predictions in Firestore: {stats['total_predictions']}")
    print(f"Average confidence: {stats['average_confidence']}%")
    
    print("\n✅ Migration complete!")
    print("\n📌 Next Steps:")
    print("   1. Verify data in Firebase Console")
    print("   2. Test your app with Firebase backend")
    print("   3. Send password reset emails to users")
    print("   4. Keep CSV backups until you're confident everything works")
    print("=" * 60)


if __name__ == "__main__":
    main()
