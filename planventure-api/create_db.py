#!/usr/bin/env python3
"""
Database initialization script for Planventure API
Run this script to create database tables
"""

import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import models after setting up the path
from models.user import db, User
from models.trip import Trip

def create_app():
    """Create Flask application for database initialization"""
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database with app
    db.init_app(app)
    
    return app

def cleanup_old_tables():
    """Remove old user_accounts table if it exists"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if user_accounts table exists and drop it
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"🔍 Found existing tables: {existing_tables}")
            
            tables_to_remove = ['user_accounts', 'planventure_users']
            
            for table_name in tables_to_remove:
                if table_name in existing_tables:
                    with db.engine.connect() as connection:
                        connection.execute(text(f'DROP TABLE {table_name}'))
                        connection.commit()
                    print(f"🗑️  Removed old {table_name} table")
                
        except Exception as e:
            print(f"⚠️  Note: {e}")

def init_database():
    """Initialize database tables"""
    print("Initializing Planventure database...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Clean up old tables first
            cleanup_old_tables()
            
            # Force drop all and recreate to ensure clean state
            db.drop_all()
            print("🗑️  Dropped all tables for clean slate")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print database info
            print(f"📍 Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # List created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tables created: {', '.join(tables)}")
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            sys.exit(1)

def drop_and_recreate():
    """Drop all tables and recreate them (WARNING: This will delete all data)"""
    print("⚠️  WARNING: This will delete all existing data!")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        app = create_app()
        
        with app.app_context():
            try:
                db.drop_all()
                print("🗑️  Dropped all existing tables")
                
                db.create_all()
                print("✅ Database tables recreated successfully!")
                
            except Exception as e:
                print(f"❌ Error recreating database: {e}")
                sys.exit(1)
    else:
        print("Operation cancelled.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        drop_and_recreate()
    else:
        init_database()
