import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.user import db, User
from models.trip import Trip

def create_app():
    """Create Flask app for database initialization"""
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def init_database():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables (optional - remove if you want to keep existing data)
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables
        db.create_all()
        print("Created all database tables")
        
        # Print table info
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("Tables created successfully!")

if __name__ == '__main__':
    init_database()
