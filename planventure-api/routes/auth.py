import re
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from models.user import db, User
from utils.auth import generate_tokens

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_email(email):
    """Validate email format using regex"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_password(password):
    """Validate password requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with email validation"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate password requirements
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email_address=email).first()
        if existing_user:
            return jsonify({
                "error": "User with this email already exists", 
                "message": "Please use a different email or try logging in instead",
                "suggestion": "Use /auth/login if you already have an account"
            }), 409
        
        # Create new user
        new_user = User(email_address=email)
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT tokens
        tokens = generate_tokens(new_user)
        
        return jsonify({
            "message": "User registered successfully",
            "user": new_user.get_user_info(),
            "tokens": tokens
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Find user by email
        user = User.query.filter_by(email_address=email).first()
        
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        if not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 401
        
        # Generate JWT tokens
        tokens = generate_tokens(user)
        
        # Add success log
        print(f"✅ User {email} logged in successfully")
        
        return jsonify({
            "message": "Login successful",
            "user": user.get_user_info(),
            "tokens": tokens
        }), 200
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@auth_bp.route('/validate-email', methods=['POST'])
def validate_email_endpoint():
    """Endpoint to validate email format"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        is_valid = validate_email(email)
        
        # Also check if email already exists
        exists = User.query.filter_by(email_address=email).first() is not None
        
        return jsonify({
            "email": email,
            "is_valid_format": is_valid,
            "already_exists": exists,
            "available": is_valid and not exists
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Validation failed: {str(e)}"}), 500
