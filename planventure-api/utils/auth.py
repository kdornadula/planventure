from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import current_app
import jwt

def generate_tokens(user):
    """
    Generate JWT access and refresh tokens for authenticated user
    
    Args:
        user (User): User model instance for whom to generate tokens
        
    Returns:
        dict: Token package containing access_token, refresh_token, and metadata
        
    Note:
        - Access token expires in 1 hour (short-lived for security)
        - Refresh token expires in 30 days (long-lived for convenience)
        - Identity is stored as string to comply with JWT standards
        - Additional claims provide extra user context in token
    """
    # Create additional claims to embed in JWT payload for convenience
    additional_claims = {
        "user_id": user.user_id,           # User's database ID
        "email": user.email_address,       # User's email for reference
        "is_active": user.is_active        # Account status at time of token creation
    }
    
    # Generate short-lived access token (used for API requests)
    # Convert user_id to string - JWT standard requires string subjects
    access_token = create_access_token(
        identity=str(user.user_id),        # JWT 'sub' claim (must be string)
        additional_claims=additional_claims, # Extra user data in token
        expires_delta=timedelta(hours=1)    # Short expiration for security
    )
    
    # Generate long-lived refresh token (used to get new access tokens)
    refresh_token = create_refresh_token(
        identity=str(user.user_id),        # Same identity as access token
        expires_delta=timedelta(days=30)    # Longer expiration for convenience
    )
    
    # Return standardized token package
    return {
        "access_token": access_token,       # For API authentication
        "refresh_token": refresh_token,     # For token renewal
        "token_type": "Bearer",            # OAuth2 standard token type
        "expires_in": 3600                 # Access token lifetime in seconds
    }

def validate_token(token):
    """
    Validate JWT token and extract user information
    
    Args:
        token (str): JWT token string to validate
        
    Returns:
        dict: Validation result with user info or error details
        
    Note:
        - Uses PyJWT library for manual token validation
        - Checks token signature against secret key
        - Verifies token hasn't expired
        - Returns structured response for error handling
    """
    try:
        # Decode and validate JWT token
        payload = jwt.decode(
            token,                                    # Token to decode
            current_app.config['JWT_SECRET_KEY'],    # Secret key for verification
            algorithms=['HS256']                     # Allowed algorithms (security measure)
        )
        
        # Return successful validation with user data
        return {
            "valid": True,
            "user_id": payload.get('sub'),          # Subject (user ID)
            "email": payload.get('email'),          # Email from additional claims
            "exp": payload.get('exp')               # Expiration timestamp
        }
    except jwt.ExpiredSignatureError:
        # Token has passed its expiration time
        return {"valid": False, "error": "Token has expired"}
    except jwt.InvalidTokenError:
        # Token is malformed, has invalid signature, etc.
        return {"valid": False, "error": "Invalid token"}
    except Exception as e:
        # Catch-all for unexpected errors
        return {"valid": False, "error": f"Token validation error: {str(e)}"}

def get_current_user_id():
    """
    Extract current user ID from JWT token in request context
    
    Returns:
        str: User ID from JWT token, or None if no valid token
        
    Note:
        - Uses Flask-JWT-Extended to extract identity from current request
        - Must be called within a request context with valid JWT
        - Returns string because JWT subjects are strings
    """
    return get_jwt_identity()

def generate_password_reset_token(user):
    """
    Generate a single-use token for password reset functionality
    
    Args:
        user (User): User requesting password reset
        
    Returns:
        str: Password reset token (JWT)
        
    Note:
        - Shorter expiration (1 hour) for security
        - Special 'type' claim to prevent token misuse
        - Uses main SECRET_KEY instead of JWT_SECRET_KEY for separation
    """
    # Create payload with user info and special type marker
    payload = {
        'user_id': user.user_id,               # User who requested reset
        'email': user.email_address,           # Email for verification
        'exp': datetime.utcnow() + timedelta(hours=1),  # 1-hour expiration
        'type': 'password_reset'               # Prevent misuse as regular JWT
    }
    
    # Generate token using main secret key (different from JWT secret)
    try:
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except TypeError:
        # Handle PyJWT version differences (some return bytes, some return strings)
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_password_reset_token(token):
    """
    Verify and extract user ID from password reset token
    
    Args:
        token (str): Password reset token to verify
        
    Returns:
        int or None: User ID if token is valid, None if invalid/expired
        
    Note:
        - Validates token type to prevent regular JWT misuse
        - Returns only user ID for minimal information exposure
        - Handles all error cases gracefully
    """
    try:
        # Decode token using main secret key
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        # Verify this is actually a password reset token
        if payload.get('type') != 'password_reset':
            return None
            
        # Return user ID for password reset
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # Token expired or invalid
        return None
    except Exception:
        # Any other error - fail safely
        return None
