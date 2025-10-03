from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import current_app
import jwt

def generate_tokens(user):
    """Generate access and refresh tokens for a user"""
    # Create additional claims for the token
    additional_claims = {
        "user_id": user.user_id,
        "email": user.email_address,
        "is_active": user.is_active
    }
    
    # Generate access token (expires in 1 hour)
    # FIX: Convert user_id to string for JWT subject
    access_token = create_access_token(
        identity=str(user.user_id),  # Convert to string here
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1)
    )
    
    # Generate refresh token (expires in 30 days)
    refresh_token = create_refresh_token(
        identity=str(user.user_id),  # Convert to string here
        expires_delta=timedelta(days=30)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 3600  # 1 hour in seconds
    }

def validate_token(token):
    """Validate JWT token and return user info"""
    try:
        # Decode the token
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        
        return {
            "valid": True,
            "user_id": payload.get('sub'),  # 'sub' is the identity
            "email": payload.get('email'),
            "exp": payload.get('exp')
        }
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}
    except Exception as e:
        return {"valid": False, "error": f"Token validation error: {str(e)}"}

def get_current_user_id():
    """Get the current user ID from JWT token"""
    return get_jwt_identity()

def generate_password_reset_token(user):
    """Generate a password reset token"""
    payload = {
        'user_id': user.user_id,
        'email': user.email_address,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'type': 'password_reset'
    }
    
    # Handle PyJWT version differences
    try:
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except TypeError:
        # For newer PyJWT versions that return string directly
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_password_reset_token(token):
    """Verify password reset token"""
    try:
        payload = jwt.decode(
            token, 
            current_app.config['SECRET_KEY'], 
            algorithms=['HS256']
        )
        
        if payload.get('type') != 'password_reset':
            return None
            
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    except Exception:
        return None
