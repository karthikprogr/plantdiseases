"""
Firebase Firestore Service Module
Handles all database operations for users, predictions, and application data
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from datetime import datetime
from typing import Optional, Dict, List, Any

# Initialize Firebase Admin SDK
_firebase_initialized = False
_db = None


def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    global _firebase_initialized, _db
    
    if _firebase_initialized:
        return _db
    
    try:
        # Option 1: Load from JSON file (local development)
        cred_path = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            print(f"[SUCCESS] Loading Firebase credentials from file: {cred_path}")
        
        # Option 2: Load from environment variable (production deployment)
        elif os.environ.get('FIREBASE_CREDENTIALS'):
            cred_json = json.loads(os.environ.get('FIREBASE_CREDENTIALS'))
            cred = credentials.Certificate(cred_json)
            print("[SUCCESS] Loading Firebase credentials from environment variable")
        
        else:
            raise ValueError("Firebase credentials not found! Set FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS env variable")
        
        # Initialize the app
        firebase_admin.initialize_app(cred)
        _db = firestore.client()
        _firebase_initialized = True
        print("[SUCCESS] Firebase Admin SDK initialized successfully")
        return _db
        
    except Exception as e:
        print(f"[ERROR] Error initializing Firebase: {e}")
        raise


def get_db():
    """Get Firestore database instance"""
    if not _firebase_initialized:
        initialize_firebase()
    return _db


# ==================== USER OPERATIONS ====================

def create_user(email: str, password: str, full_name: str, phone: str = "") -> Dict[str, Any]:
    """
    Create a new user in Firebase Auth and Firestore
    Returns: {'success': bool, 'message': str, 'user_id': str}
    """
    try:
        db = get_db()
        
        # Create user in Firebase Authentication
        user = firebase_auth.create_user(
            email=email,
            password=password,
            display_name=full_name
        )
        
        # Store additional user data in Firestore
        user_data = {
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'created_at': firestore.SERVER_TIMESTAMP,
            'last_login': firestore.SERVER_TIMESTAMP,
            'is_active': True
        }
        
        db.collection('users').document(user.uid).set(user_data)
        
        return {
            'success': True,
            'message': 'User created successfully',
            'user_id': user.uid
        }
        
    except firebase_auth.EmailAlreadyExistsError:
        return {'success': False, 'message': 'Email already exists'}
    except Exception as e:
        return {'success': False, 'message': f'Error creating user: {str(e)}'}


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get user data by email
    Returns: user dict or None
    """
    try:
        db = get_db()
        
        # Query Firestore for user with this email
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1)
        docs = query.stream()
        
        for doc in docs:
            user_data = doc.to_dict()
            user_data['user_id'] = doc.id
            return user_data
        
        return None
        
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get user data by user ID
    Returns: user dict or None
    """
    try:
        db = get_db()
        doc = db.collection('users').document(user_id).get()
        
        if doc.exists:
            user_data = doc.to_dict()
            user_data['user_id'] = doc.id
            return user_data
        
        return None
        
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None


def verify_user_password(email: str, password: str) -> Dict[str, Any]:
    """
    Verify user credentials (email + password)
    Note: Firebase Admin SDK doesn't directly verify passwords
    Use Firebase Auth REST API or client-side verification
    """
    try:
        # Get user by email
        user = firebase_auth.get_user_by_email(email)
        
        if user:
            return {
                'success': True,
                'user_id': user.uid,
                'email': user.email,
                'display_name': user.display_name
            }
        else:
            return {'success': False, 'message': 'User not found'}
            
    except Exception as e:
        return {'success': False, 'message': f'Error verifying user: {str(e)}'}


def update_user_last_login(user_id: str):
    """Update user's last login timestamp"""
    try:
        db = get_db()
        db.collection('users').document(user_id).update({
            'last_login': firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        print(f"Error updating last login: {e}")
        return False


def update_user_profile(user_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update user profile data
    updates: dict of fields to update (e.g., {'full_name': 'New Name', 'phone': '1234567890'})
    """
    try:
        db = get_db()
        db.collection('users').document(user_id).update(updates)
        return True
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return False


# ==================== PREDICTION OPERATIONS ====================

def save_prediction(user_email: str, image_name: str, prediction: str, 
                   confidence: float, supplement: str = "", 
                   description: str = "") -> str:
    """
    Save a plant disease prediction to Firestore
    Returns: prediction_id
    """
    try:
        db = get_db()
        
        prediction_data = {
            'user_email': user_email,
            'image_name': image_name,
            'prediction': prediction,
            'confidence': float(confidence),
            'supplement': supplement,
            'description': description,
            'created_at': firestore.SERVER_TIMESTAMP,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to predictions collection
        doc_ref = db.collection('predictions').add(prediction_data)
        prediction_id = doc_ref[1].id
        
        print(f"✅ Prediction saved with ID: {prediction_id}")
        return prediction_id
        
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None


def get_user_predictions(user_email: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get all predictions for a user
    Returns: list of prediction dicts
    """
    try:
        db = get_db()
        
        predictions_ref = db.collection('predictions')
        # Query without order_by to avoid index requirement
        query = predictions_ref.where('user_email', '==', user_email).limit(limit)
        
        predictions = []
        for doc in query.stream():
            pred_data = doc.to_dict()
            pred_data['prediction_id'] = doc.id
            
            # Convert Firestore timestamp to string if exists
            if 'created_at' in pred_data and pred_data['created_at']:
                try:
                    pred_data['created_at'] = pred_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pred_data['created_at'] = str(pred_data['created_at'])
            
            predictions.append(pred_data)
        
        # Sort in Python instead of Firestore
        predictions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return predictions
        
    except Exception as e:
        print(f"Error getting user predictions: {e}")
        return []


def get_prediction_by_id(prediction_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific prediction by ID"""
    try:
        db = get_db()
        doc = db.collection('predictions').document(prediction_id).get()
        
        if doc.exists:
            pred_data = doc.to_dict()
            pred_data['prediction_id'] = doc.id
            return pred_data
        
        return None
        
    except Exception as e:
        print(f"Error getting prediction: {e}")
        return None


def delete_prediction(prediction_id: str) -> bool:
    """Delete a prediction"""
    try:
        db = get_db()
        db.collection('predictions').document(prediction_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False


# ==================== PASSWORD RESET OPERATIONS ====================

def save_password_reset_token(email: str, token: str, expiry: datetime):
    """Save password reset token"""
    try:
        db = get_db()
        
        reset_data = {
            'email': email,
            'token': token,
            'expiry': expiry,
            'used': False,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('password_resets').document(token).set(reset_data)
        return True
        
    except Exception as e:
        print(f"Error saving reset token: {e}")
        return False


def get_password_reset_token(token: str) -> Optional[Dict[str, Any]]:
    """Get password reset token data"""
    try:
        db = get_db()
        doc = db.collection('password_resets').document(token).get()
        
        if doc.exists:
            return doc.to_dict()
        return None
        
    except Exception as e:
        print(f"Error getting reset token: {e}")
        return None


def mark_reset_token_used(token: str):
    """Mark password reset token as used"""
    try:
        db = get_db()
        db.collection('password_resets').document(token).update({'used': True})
        return True
    except Exception as e:
        print(f"Error marking token as used: {e}")
        return False


# ==================== STATISTICS & ANALYTICS ====================

def get_prediction_stats(user_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Get statistics about predictions
    If user_email provided, returns stats for that user only
    """
    try:
        db = get_db()
        
        predictions_ref = db.collection('predictions')
        
        if user_email:
            query = predictions_ref.where('user_email', '==', user_email)
        else:
            query = predictions_ref
        
        predictions = list(query.stream())
        
        # Calculate statistics
        total_predictions = len(predictions)
        
        disease_counts = {}
        confidence_sum = 0
        
        for doc in predictions:
            data = doc.to_dict()
            prediction = data.get('prediction', 'Unknown')
            confidence = data.get('confidence', 0)
            
            disease_counts[prediction] = disease_counts.get(prediction, 0) + 1
            confidence_sum += confidence
        
        avg_confidence = (confidence_sum / total_predictions) if total_predictions > 0 else 0
        
        return {
            'total_predictions': total_predictions,
            'disease_distribution': disease_counts,
            'average_confidence': round(avg_confidence, 2),
            'most_common_disease': max(disease_counts, key=disease_counts.get) if disease_counts else None
        }
        
    except Exception as e:
        print(f"Error getting prediction stats: {e}")
        return {
            'total_predictions': 0,
            'disease_distribution': {},
            'average_confidence': 0,
            'most_common_disease': None
        }


# ==================== UTILITY FUNCTIONS ====================

def test_firebase_connection() -> bool:
    """Test Firebase connection"""
    try:
        db = get_db()
        # Try to read from a collection (won't fail even if empty)
        db.collection('_test').limit(1).get()
        print("[SUCCESS] Firebase connection successful")
        return True
    except Exception as e:
        print(f"[ERROR] Firebase connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing Firebase connection...")
    test_firebase_connection()
