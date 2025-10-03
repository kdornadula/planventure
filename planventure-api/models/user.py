from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_address = db.Column(db.String(150), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(300), nullable=False)
    account_created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<User({self.user_id}): {self.email_address}>'
    
    def set_password(self, password):
        """Hash and set the user's password"""
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.hashed_password = password_hash.decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        if not self.hashed_password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def update_timestamp(self):
        """Update the last modified timestamp"""
        self.last_updated_at = datetime.utcnow()
    
    def get_user_info(self):
        """Returns user information as dictionary (excluding password)"""
        return {
            'user_id': self.user_id,
            'email_address': self.email_address,
            'account_created_at': self.account_created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated_at': self.last_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }
    
    @staticmethod
    def generate_password_hash(password):
        """Static method to generate password hash (utility function)"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """Static method to verify password against hash (utility function)"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
