"""
Database models for Plant Disease Detection System
Uses SQLAlchemy ORM for better data management
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User account model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Prediction(db.Model):
    """Prediction history model"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Image info
    image_path = db.Column(db.String(300), nullable=False)
    original_filename = db.Column(db.String(200))
    
    # Prediction results
    predicted_class = db.Column(db.Integer, nullable=False)
    disease_name = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    is_valid_plant = db.Column(db.Boolean, default=True)
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))  # Supports IPv6
    user_agent = db.Column(db.String(300))
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='prediction', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'disease_name': self.disease_name,
            'confidence': round(self.confidence * 100, 1),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'image_path': self.image_path,
            'is_healthy': self.predicted_class in [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
        }
    
    def __repr__(self):
        return f'<Prediction {self.id}: {self.disease_name}>'


class Feedback(db.Model):
    """User feedback on predictions"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'), nullable=True, index=True)
    
    # Feedback data
    rating = db.Column(db.Integer)  # 1-5 stars, or 0 for thumbs down, 1 for thumbs up
    is_helpful = db.Column(db.Boolean)  # True = thumbs up, False = thumbs down
    comment = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)  # Was the prediction correct?
    actual_disease = db.Column(db.String(200))  # If incorrect, what was it?
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id}: {"👍" if self.is_helpful else "👎"}>'


class SystemLog(db.Model):
    """System activity and error logs"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))  # INFO, WARNING, ERROR
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Log {self.level}: {self.message[:50]}>'


# Helper functions
def init_db(app):
    """Initialize database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")


def migrate_csv_to_db(app):
    """Migrate existing CSV data to database"""
    import csv
    import os
    
    with app.app_context():
        # Migrate users from CSV
        users_csv = 'users.csv'
        if os.path.exists(users_csv):
            print("📊 Migrating users from CSV...")
            with open(users_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        username, password_hash = row[0], row[1]
                        
                        # Check if user already exists
                        if not User.query.filter_by(username=username).first():
                            user = User(
                                username=username,
                                password_hash=password_hash,
                                created_at=datetime.utcnow()
                            )
                            db.session.add(user)
            
            db.session.commit()
            print(f"✅ Migrated {User.query.count()} users")
        else:
            print("ℹ️  No users.csv found, skipping user migration")
        
        print("✅ Database migration complete!")


def get_user_stats(user_id):
    """Get statistics for a user"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    total_predictions = user.predictions.count()
    healthy_count = user.predictions.filter(
        Prediction.predicted_class.in_([3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38])
    ).count()
    diseased_count = total_predictions - healthy_count
    
    return {
        'total_predictions': total_predictions,
        'healthy_plants': healthy_count,
        'diseased_plants': diseased_count,
        'member_since': user.created_at.strftime('%B %Y'),
        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'
    }
