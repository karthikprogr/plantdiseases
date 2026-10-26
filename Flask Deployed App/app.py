import os
import csv
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, render_template, request, url_for, session, jsonify, flash
from werkzeug.utils import secure_filename
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from openai import OpenAI

# -------------------- Load Environment --------------------
load_dotenv()

# -------------------- Config --------------------
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
USERS_CSV = 'users.csv'
MODEL_PATH = "plant_disease_model_1_latest.pt"

# Email configuration
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# -------------------- Load Data and Model --------------------
try:
    disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
except Exception as e:
    print(f"Error loading disease_info.csv: {e}")
    disease_info = pd.DataFrame()

try:
    supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')
except Exception as e:
    print(f"Error loading supplement_info.csv: {e}")
    supplement_info = pd.DataFrame()

# Load model
device = torch.device('cpu')
try:
    model = CNN.CNN(39)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"Error loading model from {MODEL_PATH}: {e}")
    model = None


def prediction(image_path):
    """
    Return predicted class index (int) and confidence score (float) for the given image path.
    Returns: (predicted_index, confidence_score, is_valid_plant_image)
    """
    if model is None:
        raise RuntimeError("Model not loaded.")
    
    # Load and convert image to RGB
    image = Image.open(image_path).convert("RGB")
    
    # Apply the SAME transformations used during training
    # Resize to 255, then center crop to 224 (matches training pipeline)
    image = image.resize((255, 255), Image.Resampling.LANCZOS)  # High-quality resize
    
    # Center crop to 224x224 (same as training)
    width, height = image.size
    left = (width - 224) / 2
    top = (height - 224) / 2
    right = (width + 224) / 2
    bottom = (height + 224) / 2
    image = image.crop((left, top, right, bottom))
    
    # Convert to tensor (NO NORMALIZATION - model was trained without it!)
    input_data = TF.to_tensor(image)
    
    # Add batch dimension
    input_data = input_data.unsqueeze(0)
    
    # Predict
    with torch.no_grad():
        output = model(input_data)
    
    if isinstance(output, torch.Tensor):
        output = output.cpu().numpy()
    
    # Apply softmax to get probabilities (using numpy)
    exp_output = np.exp(output[0] - np.max(output[0]))  # Subtract max for numerical stability
    probabilities = exp_output / np.sum(exp_output)
    
    # Get predicted class and confidence
    index = int(np.argmax(probabilities))
    confidence = float(probabilities[index])
    
    # 🔧 TEMPORARY: DISABLE VALIDATION TO SEE ALL PREDICTIONS
    # Validation: Check if this is a valid plant image
    is_valid_plant = True  # Always accept for debugging
    
    # Print all probabilities for debugging
    print(f"🔍 DEBUG: Top 5 predictions:")
    top_5_indices = np.argsort(probabilities)[-5:][::-1]
    for i, idx in enumerate(top_5_indices, 1):
        print(f"   {i}. Class {idx} ({CNN.idx_to_classes.get(int(idx), 'Unknown')}): {probabilities[idx]*100:.2f}%")
    
    # Original validation logic (commented out for debugging)
    # # Check 1: If predicted as "Background without leaves" (class 4) with high confidence
    # if index == 4 and confidence > 0.40:
    #     is_valid_plant = False
    # 
    # # Check 2: If confidence is extremely low (< 15%), likely not a plant from our dataset
    # elif confidence < 0.15:
    #     is_valid_plant = False
    # 
    # # Check 3: If background probability is very high (> 50%)
    # elif probabilities[4] > 0.50:
    #     is_valid_plant = False
    
    return index, confidence, is_valid_plant


# -------------------- Flask App --------------------
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_this_secret_in_prod")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------------------- Database Configuration --------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant_disease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # Set to True for SQL query logging

# Import and initialize database
from models import db, init_db, User, Prediction, Feedback, migrate_csv_to_db, get_user_stats
init_db(app)

# -------------------- Google OAuth Configuration --------------------
from authlib.integrations.flask_client import OAuth

# Import credentials from config file (easier to edit)
try:
    from config_oauth import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FLASK_SECRET_KEY
    # Use credentials from config file
    app.config['GOOGLE_CLIENT_ID'] = GOOGLE_CLIENT_ID
    app.config['GOOGLE_CLIENT_SECRET'] = GOOGLE_CLIENT_SECRET
    app.secret_key = FLASK_SECRET_KEY  # Update secret key
    print("✅ Google OAuth credentials loaded from config_oauth.py")
except ImportError:
    # Fallback to environment variables if config file doesn't exist
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
    print("⚠️  Using default credentials. Edit config_oauth.py to add your Google credentials.")

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Migrate CSV data on first run (comment out after first migration)
# with app.app_context():
#     migrate_csv_to_db(app)

# -------------------- OpenAI Setup --------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not set! Chatbot will not work.")
    client = None
else:
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI client initialized.")

# -------------------- Token Serializer --------------------
s = URLSafeTimedSerializer(app.secret_key)


# -------------------- Helpers --------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_users():
    users = []
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    users.append([row[0], row[1]])
    return users


def append_user(username, password):
    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        hashed_password = generate_password_hash(password)
        writer.writerow([username, hashed_password])


def update_user_password(username, new_password):
    """Updates a user's password in the CSV file."""
    users = []
    user_found = False
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    if row[0] == username:
                        hashed_password = generate_password_hash(new_password)
                        users.append([username, hashed_password])
                        user_found = True
                    else:
                        users.append(row)
    
    if user_found:
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(users)
    return user_found


def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = MAIL_USERNAME
    msg['To'] = to_email
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)


# -------------------- Chatbot API Route --------------------
@app.route('/chat', methods=['POST'])
def chat():
    if client is None:
        return jsonify({'error': 'OpenAI API key not set.'}), 500

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400

    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided.'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change to "gpt-4-turbo" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant for plant disease detection."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({'response': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------- Routes --------------------
@app.route('/')
def login_default():
    if 'username' in session:
        return redirect(url_for('home_page'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Database-based authentication
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                return render_template('login.html', error="Account is deactivated. Contact support.")
            
            # Update last login
            user.last_login = datetime.now()
            db.session.commit()
            
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('home_page'))

        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not all([username, password]):
            return render_template('signup.html', error="Please provide both an email and password.")

        # Password strength validation
        if len(password) < 6:
            return render_template('signup.html', error="Password must be at least 6 characters long.")

        # Add email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            return render_template('signup.html', error="Invalid email address format. Please enter a valid email.")

        # Database-based signup
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error="An account with this email already exists.")

        # Create new user
        new_user = User(username=username, email=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/google-login')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/google-authorize')
def google_authorize():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user information from Google', 'danger')
            return redirect(url_for('login'))
        
        # Extract user information
        email = user_info.get('email')
        name = user_info.get('name')
        google_id = user_info.get('sub')  # Google's unique user ID
        
        if not email:
            flash('Email not provided by Google', 'danger')
            return redirect(url_for('login'))
        
        # Check if user exists with this email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user account
            # Generate username from email (before @)
            username = email.split('@')[0]
            
            # Make sure username is unique
            counter = 1
            original_username = username
            while User.query.filter_by(username=username).first():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Create new user with a random password (won't be used for Google login)
            import secrets
            user = User(
                username=username,
                email=email
            )
            user.set_password(secrets.token_urlsafe(32))  # Random secure password
            user.last_login = datetime.now()
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'Welcome {name}! Your account has been created.', 'success')
        else:
            # Update existing user's last login
            user.last_login = datetime.now()
            db.session.commit()
            
            flash(f'Welcome back {name}!', 'success')
        
        # Set session
        session['username'] = user.username
        session['user_id'] = user.id
        session['google_user'] = True  # Mark as Google authenticated user
        
        return redirect(url_for('home_page'))
    
    except Exception as e:
        print(f"Google OAuth Error: {e}")
        flash('An error occurred during Google sign-in. Please try again.', 'danger')
        return redirect(url_for('login'))


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Handle user feedback submission"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to submit feedback'}), 401
    
    try:
        data = request.get_json()
        prediction_id = data.get('prediction_id') or session.get('last_prediction_id')
        
        if not prediction_id:
            return jsonify({'success': False, 'message': 'No prediction found'}), 400
        
        # Create feedback record
        feedback = Feedback(
            user_id=session['user_id'],
            prediction_id=prediction_id,
            rating=data.get('rating', 0),
            is_helpful=data.get('is_helpful', True),
            comment=data.get('comment', ''),
            is_correct=data.get('is_correct', True),
            actual_disease=data.get('actual_disease', '')
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Thank you for your feedback!'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/history')
def prediction_history():
    """Display user's prediction history"""
    if 'user_id' not in session:
        flash('Please login to view your history', 'warning')
        return redirect(url_for('login'))
    
    try:
        # DEBUG: Print session information
        print("\n" + "="*70)
        print("🔍 HISTORY PAGE DEBUG")
        print("="*70)
        user_id = session.get('user_id')
        print(f"📋 Session user_id: {user_id}")
        print(f"📋 Session user_id type: {type(user_id)}")
        print(f"📋 Full session data: {dict(session)}")
        
        # DEBUG: Test direct query
        test_query = Prediction.query.filter_by(user_id=user_id).all()
        print(f"🔎 Direct query result: Found {len(test_query)} predictions")
        
        # DEBUG: Test with type conversion
        if isinstance(user_id, str):
            print(f"⚠️  user_id is string! Converting to int...")
            user_id_int = int(user_id)
            test_query2 = Prediction.query.filter_by(user_id=user_id_int).all()
            print(f"🔎 Query with int conversion: Found {len(test_query2)} predictions")
        
        # DEBUG: Check if user exists
        user = User.query.get(user_id)
        print(f"👤 User object: {user}")
        if user:
            print(f"👤 User.username: {user.username}")
            print(f"👤 User.predictions.count(): {user.predictions.count()}")
        
        print("="*70 + "\n")
        
        # Get user statistics (with safe defaults)
        try:
            stats = get_user_stats(session['user_id'])
            print(f"📊 Stats from get_user_stats: {stats}")
        except Exception as stats_error:
            print(f"❌ Stats error: {stats_error}")
            import traceback
            traceback.print_exc()
            # Provide default stats if there's an error
            stats = {
                'total_predictions': 0,
                'healthy_plants': 0,
                'diseased_plants': 0,
                'member_since': 'Unknown',
                'last_login': 'Never'
            }
        
        # Get recent predictions with pagination and filtering
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Start with base query
        query = Prediction.query.filter_by(user_id=session['user_id'])
        
        # Apply search filter
        search_term = request.args.get('search', '').strip()
        if search_term:
            query = query.filter(Prediction.disease_name.ilike(f'%{search_term}%'))
            print(f"🔍 Applying search filter: {search_term}")
        
        # Apply health filter
        health_filter = request.args.get('health', '')
        if health_filter == 'healthy':
            # Filter for healthy plant classes (based on your model's healthy class indices)
            healthy_classes = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
            query = query.filter(Prediction.predicted_class.in_(healthy_classes))
            print(f"🌱 Applying health filter: healthy only")
        elif health_filter == 'diseased':
            # Filter for diseased plant classes
            healthy_classes = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
            query = query.filter(~Prediction.predicted_class.in_(healthy_classes))
            print(f"🦠 Applying health filter: diseased only")
        
        # Apply sorting
        sort_by = request.args.get('sort', 'newest')
        if sort_by == 'oldest':
            query = query.order_by(Prediction.timestamp.asc())
            print(f"📅 Sorting by: oldest first")
        elif sort_by == 'confidence':
            query = query.order_by(Prediction.confidence.desc())
            print(f"📊 Sorting by: highest confidence")
        else:  # newest (default)
            query = query.order_by(Prediction.timestamp.desc())
            print(f"📅 Sorting by: newest first")
        
        # Execute query with pagination
        predictions = query.paginate(page=page, per_page=per_page, error_out=False)
        
        print(f"✅ History page: Found {predictions.total} predictions for user {session['user_id']}")
        if search_term or health_filter or sort_by:
            print(f"🎯 Filters active - Showing {len(predictions.items)} results on page {page}")
        
        return render_template('history.html',
                             username=session.get('username', 'User'),
                             predictions=predictions.items,
                             stats=stats,
                             pagination=predictions,
                             total=predictions.total)
    
    except Exception as e:
        print(f"❌ History page error: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error loading history: {str(e)}', 'danger')
        # Return an empty history page instead of redirecting
        return render_template('history.html',
                             username=session.get('username', 'User'),
                             predictions=[],
                             stats={'total_predictions': 0, 'healthy_plants': 0, 'diseased_plants': 0, 'member_since': 'Unknown', 'last_login': 'Never'},
                             pagination=None,
                             total=0)


@app.route('/delete-prediction/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    """Delete a prediction from history"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        prediction = Prediction.query.filter_by(id=prediction_id, user_id=session['user_id']).first()
        
        if not prediction:
            return jsonify({'success': False, 'message': 'Prediction not found'}), 404
        
        # Delete the image file if it exists
        try:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(prediction.image_path))
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as file_error:
            print(f"Warning: Could not delete image file: {file_error}")
        
        # Delete from database
        db.session.delete(prediction)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Prediction deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/debug-session')
def debug_session():
    """Debug route to check session and database state"""
    output = "<h1>🔍 Debug Information</h1>"
    output += "<style>body{font-family:monospace;padding:20px;} .info{background:#e3f2fd;padding:10px;margin:10px 0;} .error{background:#ffebee;padding:10px;margin:10px 0;}</style>"
    
    # Session info
    output += "<div class='info'><h2>Session Data:</h2>"
    if session:
        for key, value in session.items():
            output += f"<b>{key}:</b> {value} (type: {type(value).__name__})<br>"
    else:
        output += "No session data"
    output += "</div>"
    
    # Check if logged in
    if 'user_id' in session:
        user_id = session['user_id']
        output += f"<div class='info'><h2>User ID from session: {user_id} (type: {type(user_id).__name__})</h2></div>"
        
        # Get user
        user = User.query.get(user_id)
        output += "<div class='info'><h2>User Object:</h2>"
        if user:
            output += f"ID: {user.id}<br>Username: {user.username}<br>Email: {user.email}<br>"
        else:
            output += "<span style='color:red'>User not found!</span>"
        output += "</div>"
        
        # Direct query for predictions
        output += "<div class='info'><h2>Direct Database Query:</h2>"
        predictions = Prediction.query.filter_by(user_id=user_id).all()
        output += f"<b>Found {len(predictions)} predictions</b><br><br>"
        for p in predictions[:5]:  # Show first 5
            output += f"ID: {p.id}, Disease: {p.disease_name}, Confidence: {p.confidence:.2f}, Time: {p.timestamp}<br>"
        output += "</div>"
        
        # Try get_user_stats
        output += "<div class='info'><h2>get_user_stats() Result:</h2>"
        try:
            stats = get_user_stats(user_id)
            if stats:
                for key, value in stats.items():
                    output += f"<b>{key}:</b> {value}<br>"
            else:
                output += "<span style='color:red'>get_user_stats returned None</span>"
        except Exception as e:
            output += f"<span style='color:red'>Error: {str(e)}</span>"
        output += "</div>"
    else:
        output += "<div class='error'>Not logged in - no user_id in session</div>"
    
    # All users
    output += "<div class='info'><h2>All Users in Database:</h2>"
    all_users = User.query.all()
    for u in all_users:
        pred_count = Prediction.query.filter_by(user_id=u.id).count()
        output += f"ID: {u.id}, Username: {u.username}, Email: {u.email}, Predictions: {pred_count}<br>"
    output += "</div>"
    
    return output


@app.route('/home')
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])


@app.route('/debug-info')
def debug_info():
    """Debug route to check session and predictions"""
    if 'user_id' not in session:
        return jsonify({
            'error': 'Not logged in',
            'session': dict(session)
        })
    
    from models import Prediction
    user_predictions = Prediction.query.filter_by(user_id=session['user_id']).all()
    
    return jsonify({
        'logged_in_as': session.get('username'),
        'user_id': session.get('user_id'),
        'total_predictions': len(user_predictions),
        'recent_predictions': [
            {
                'id': p.id,
                'disease': p.disease_name,
                'confidence': f"{p.confidence*100:.1f}%",
                'date': str(p.timestamp)
            }
            for p in user_predictions[:5]
        ],
        'all_session_data': dict(session)
    })


@app.route('/test-history')
def test_history_page():
    """Interactive debug page for testing history feature"""
    return render_template('debug_history.html')


@app.route('/simple-upload')
def simple_upload_page():
    """Simplest possible upload form for testing"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('simple_upload.html')


@app.route('/index')
def ai_engine_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/market')
def market():
    if 'username' not in session:
        return redirect(url_for('login'))

    supp_img = list(supplement_info.get('supplement image', []))
    supp_name = list(supplement_info.get('supplement name', []))
    disease = list(disease_info.get('disease_name', []))
    buy_links = list(supplement_info.get('buy link', []))

    return render_template(
        'market.html',
        supplement_image=supp_img,
        supplement_name=supp_name,
        disease=disease,
        buy=buy_links
    )


@app.route('/contact')
def contact():
    return render_template('contact-us.html')


@app.route('/services')
def services():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('services.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not all([email, new_password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('forgot_password'))

        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('forgot_password'))

        # You can add more robust password validation here if needed
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('forgot_password'))

        users = read_users()
        user_exists = any(u == email for u, _ in users)

        if user_exists:
            if update_user_password(email, new_password):
                flash('Your password has been reset successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An unexpected error occurred while updating the password.', 'error')
        else:
            flash('Email address not found.', 'error')
        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Token expires after 1 hour (3600 seconds)
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash("The password reset link has expired.", "error")
        return redirect(url_for('forgot_password'))
    except BadTimeSignature:
        flash("Invalid password reset link.", "error")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password', token=token))

        if update_user_password(email, password):
            flash('Your password has been successfully reset!', 'success')
            return redirect(url_for('login'))
        else:
            flash("Could not update password. User not found.", "error")
            return redirect(url_for('reset_password', token=token))

    return render_template('reset_password.html', token=token)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print(f"🚀 SUBMIT ROUTE CALLED! Method: {request.method}")
    print(f"🔐 Session keys: {list(session.keys())}")
    print(f"📁 Files in request: {list(request.files.keys())}")
    
    if 'username' not in session:
        print("⚠️ User not logged in, redirecting to login")
        return redirect(url_for('login'))
    
    print(f"📊 Submit route accessed by user: {session.get('username')} (ID: {session.get('user_id')})")
    
    # Helper function to render submit.html with default values for errors
    def render_submit_error(error_message, confidence=0, uploaded_image=""):
        return render_template('submit.html',
                             error=error_message,
                             confidence=confidence,
                             title="",
                             desc="",
                             prevent="",
                             image_url="",
                             pred=0,
                             sname="",
                             simage="",
                             buy_link="",
                             uploaded_image=uploaded_image)

    if request.method == 'POST':
        if 'image' not in request.files:
            return render_submit_error("No file part in request")

        image = request.files['image']
        if image.filename == '':
            return render_submit_error("No image selected")

        if not allowed_file(image.filename):
            return render_submit_error("Unsupported file type. Please upload PNG, JPG, or JPEG files only.")

        # Generate unique filename with timestamp to avoid overwriting
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(image.filename)
        filename = f"{timestamp}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(file_path)

        try:
            pred, confidence, is_valid_plant = prediction(file_path)
            print(f"🔍 Prediction: class={pred}, confidence={confidence:.2%}, valid={is_valid_plant}")
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return render_submit_error(f"Prediction failed: {e}")

        # Save prediction to database - ALWAYS SAVE REGARDLESS OF VALIDITY
        user_id = session.get('user_id')
        if user_id:
            disease_name = CNN.idx_to_classes.get(pred, "Unknown")
            print(f"💾 Saving prediction for user {user_id}: {disease_name}")
            
            try:
                new_prediction = Prediction(
                    user_id=user_id,
                    image_path=f'uploads/{filename}',
                    original_filename=original_filename,
                    predicted_class=pred,
                    disease_name=disease_name,
                    confidence=confidence,
                    is_valid_plant=is_valid_plant,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent', '')[:300]
                )
                db.session.add(new_prediction)
                db.session.commit()
                
                # Store prediction ID in session for feedback
                session['last_prediction_id'] = new_prediction.id
                print(f"✅ Prediction saved with ID: {new_prediction.id}")
            except Exception as db_error:
                print(f"❌ Database save error: {db_error}")
                db.session.rollback()
        else:
            print(f"⚠️ No user_id in session! Session keys: {list(session.keys())}")

        # Check if the image is a valid plant from our dataset
        if not is_valid_plant:
            # Get list of supported plants for the error message
            supported_plants = """
            <strong>Supported Plants:</strong><br>
            🍎 Apple, 🍒 Cherry, 🌽 Corn, 🍇 Grape, 🍊 Orange<br>
            🍑 Peach, 🌶️ Pepper (Bell), 🥔 Potato, 🫐 Raspberry, 🫘 Soybean<br>
            🎃 Squash, 🍓 Strawberry, 🍅 Tomato, 🫐 Blueberry
            """
            error_message = f"""
            <div style='text-align: center; padding: 20px;'>
                <h4 style='color: #d32f2f;'>⚠️ Invalid Image Detected</h4>
                <p>The uploaded image does not appear to be a plant leaf from our supported dataset.</p>
                <p><strong>Confidence Score:</strong> {confidence*100:.1f}%</p>
                <hr>
                {supported_plants}
                <hr>
                <p style='margin-top: 15px;'><strong>💡 Tips:</strong></p>
                <ul style='text-align: left; display: inline-block;'>
                    <li>Use a clear image of a single plant leaf</li>
                    <li>Ensure good lighting and focus</li>
                    <li>Select a plant from the supported list above</li>
                    <li>Refer to the plant cards on the <a href='/home'>Home Page</a></li>
                </ul>
            </div>
            """
            return render_submit_error(error_message, 
                                      confidence=confidence,
                                      uploaded_image=url_for('static', filename=f'uploads/{filename}'))

        def safe_get(df, col, idx):
            if col not in df.columns or idx >= len(df):
                return ""
            return df.iloc[idx][col]

        title = safe_get(disease_info, 'disease_name', pred)
        description = safe_get(disease_info, 'description', pred)
        prevent = safe_get(disease_info, 'Possible Steps', pred)
        image_url = safe_get(disease_info, 'image_url', pred)

        supplement_name = safe_get(supplement_info, 'supplement name', pred)
        supplement_image_url = safe_get(supplement_info, 'supplement image', pred)
        supplement_buy_link = safe_get(supplement_info, 'buy link', pred)

        # Create URL for the uploaded image to display it in results
        uploaded_image_url = url_for('static', filename=f'uploads/{filename}')

        return render_template(
            'submit.html',
            title=title,
            desc=description,
            prevent=prevent,
            image_url=image_url,
            pred=pred,
            sname=supplement_name,
            simage=supplement_image_url,
            buy_link=supplement_buy_link,
            uploaded_image=uploaded_image_url,  # NEW: Pass uploaded image URL
            confidence=confidence  # NEW: Pass confidence score
        )

    # GET request - show empty form with default values
    return render_template('submit.html',
                         confidence=0,
                         title="",
                         desc="",
                         prevent="",
                         image_url="",
                         pred=0,
                         sname="",
                         simage="",
                         buy_link="",
                         uploaded_image="")


# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
