from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# Initialize SQLAlchemy instance for database operations
db = SQLAlchemy()

class User(db.Model):
    """
    User model for handling user accounts and authentication
    
    This model stores user information including email, hashed passwords,
    and account metadata. It provides methods for password hashing/verification
    and user information retrieval.
    """
    __tablename__ = 'users'  # Explicit table name in database
    
    # PRIMARY KEY AND IDENTIFICATION
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique user identifier
    email_address = db.Column(db.String(150), unique=True, nullable=False, index=True)  # User's email (indexed for fast lookups)
    
    # SECURITY FIELDS
    hashed_password = db.Column(db.String(300), nullable=False)  # Bcrypt hashed password (never store plain text)
    
    # METADATA AND TIMESTAMPS
    account_created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Account creation timestamp
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Auto-update on changes
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Account status (for deactivation without deletion)
    
    def __repr__(self):
        """String representation for debugging and logging"""
        return f'<User({self.user_id}): {self.email_address}>'
    
    # PASSWORD MANAGEMENT METHODS
    def set_password(self, password):
        """
        Hash and store user password securely using bcrypt
        
        Args:
            password (str): Plain text password to hash
            
        Note:
            - Generates unique salt for each password
            - Uses bcrypt for secure, slow hashing
            - Stores only the hash, never the plain text
        """
        # Generate cryptographically secure salt
        salt = bcrypt.gensalt()
        # Hash password with salt using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        # Store as string in database
        self.hashed_password = password_hash.decode('utf-8')
    
    def check_password(self, password):
        """
        Verify provided password against stored hash
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
            
        Note:
            - Uses bcrypt's secure comparison to prevent timing attacks
            - Returns False if no password hash is stored
        """
        if not self.hashed_password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    # UTILITY METHODS
    def update_timestamp(self):
        """Manually update the last modified timestamp"""
        self.last_updated_at = datetime.utcnow()
    
    def get_user_info(self):
        """
        Return user information as dictionary (excluding sensitive data)
        
        Returns:
            dict: User information safe for API responses
            
        Note:
            - Excludes password hash for security
            - Formats timestamps as readable strings
            - Safe to return in API responses
        """
        return {
            'user_id': self.user_id,
            'email_address': self.email_address,
            'account_created_at': self.account_created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated_at': self.last_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }
    
    # STATIC UTILITY METHODS (can be called without User instance)
    @staticmethod
    def generate_password_hash(password):
        """
        Static method to generate password hash without creating User instance
        
        Args:
            password (str): Plain text password to hash
            
        Returns:
            str: Bcrypt hashed password
            
        Use case: For testing or external password hashing
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """
        Static method to verify password against hash without User instance
        
        Args:
            password (str): Plain text password
            password_hash (str): Stored bcrypt hash
            
        Returns:
            bool: True if password matches hash
            
        Use case: For testing or external password verification
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
