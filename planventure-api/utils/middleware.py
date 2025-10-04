from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.user import User, db
import jwt as pyjwt

def auth_required(optional=False):
    """
    Decorator to protect routes with JWT authentication
    
    This is the main authentication middleware that can be applied to any route
    to require or optionally check for JWT authentication.
    
    Args:
        optional (bool): If True, allows access without token but provides user context if token exists
                        If False, requires valid JWT token for access
                        
    Returns:
        function: Decorated function with authentication logic
        
    Usage:
        @auth_required()          # Requires valid JWT token
        @auth_required(optional=True)  # Optional authentication
        
    Note:
        - For required auth: Returns 401 if no/invalid token
        - For optional auth: Continues execution even without token
        - Handles token validation, user lookup, and account status checks
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                print(f"🔍 Debug - auth_required called, optional={optional}")
                
                if optional:
                    # OPTIONAL AUTHENTICATION FLOW
                    # Allow access without token, but provide user context if token exists
                    verify_jwt_in_request(optional=True)  # Don't fail if no token
                    current_user_id = get_jwt_identity()
                    print(f"🔍 Debug - optional auth, user_id: {current_user_id} (type: {type(current_user_id)})")
                    
                    if current_user_id:
                        # Token exists - validate user and account status
                        # Convert string user_id to integer for database lookup
                        if isinstance(current_user_id, str):
                            try:
                                current_user_id = int(current_user_id)
                            except ValueError:
                                print(f"❌ Could not convert user_id to int: {current_user_id}")
                                return f(*args, **kwargs)  # Continue without auth for optional
                        
                        # Check if user exists and is active
                        user = User.query.filter_by(user_id=current_user_id).first()
                        if user and not user.is_active:
                            return jsonify({"error": "User account is inactive"}), 401
                else:
                    # REQUIRED AUTHENTICATION FLOW
                    # Must have valid token to proceed
                    print("🔍 Debug - verifying JWT...")
                    verify_jwt_in_request()  # Will raise exception if no/invalid token
                    current_user_id = get_jwt_identity()
                    print(f"🔍 Debug - required auth, user_id: {current_user_id} (type: {type(current_user_id)})")
                    
                    # Validate user identity exists in token
                    if not current_user_id:
                        return jsonify({"error": "Invalid token: no user identity"}), 401
                    
                    # Convert string user_id to integer for database lookup
                    if isinstance(current_user_id, str):
                        try:
                            current_user_id = int(current_user_id)
                        except ValueError:
                            return jsonify({"error": "Invalid user ID format"}), 401
                    
                    # Verify user exists in database
                    user = User.query.filter_by(user_id=current_user_id).first()
                    print(f"🔍 Debug - found user: {user}")
                    
                    if not user:
                        return jsonify({"error": "User not found"}), 401
                    
                    # Check if account is active (not deactivated)
                    if not user.is_active:
                        return jsonify({"error": "Account is deactivated"}), 401
                
                # Authentication successful - proceed to route
                print("🔍 Debug - authentication successful, calling route")
                return f(*args, **kwargs)
                
            except Exception as e:
                # Handle authentication errors
                print(f"❌ Debug - Exception in auth_required: {e}")
                print(f"❌ Debug - Exception type: {type(e)}")
                
                if optional:
                    # For optional auth, continue without authentication on error
                    return f(*args, **kwargs)
                # For required auth, return error
                return jsonify({"error": f"Authentication failed: {str(e)}"}), 401
                
        return decorated_function
    return decorator

def get_current_user():
    """
    Get the current authenticated user from JWT token in request context
    
    Returns:
        User: User model instance if authenticated, None otherwise
        
    Note:
        - Must be called within a request context with valid JWT
        - Handles string to integer conversion for user_id lookup
        - Returns None if any step fails (no token, invalid user_id, user not found)
        - Safe to call from any route - won't raise exceptions
        
    Usage:
        current_user = get_current_user()
        if current_user:
            print(f"Authenticated as: {current_user.email_address}")
    """
    try:
        # Extract user identity from JWT token in current request
        current_user_id = get_jwt_identity()
        print(f"🔍 Debug - current_user_id from token: {current_user_id} (type: {type(current_user_id)})")
        
        if current_user_id:
            # Convert string user_id to integer for database lookup
            # JWT subjects are strings, but our user_id is integer
            if isinstance(current_user_id, str):
                try:
                    current_user_id = int(current_user_id)
                except ValueError:
                    print(f"❌ Could not convert user_id to int: {current_user_id}")
                    return None
            
            # Look up user in database
            user = User.query.filter_by(user_id=current_user_id).first()
            print(f"🔍 Debug - found user: {user}")
            return user
    except Exception as e:
        # Log error but don't raise - this function should be safe to call
        print(f"❌ Error getting current user: {e}")
    return None

def require_active_user(f):
    """
    Decorator that requires an active user account (stricter than auth_required)
    
    This decorator not only requires authentication but also explicitly checks
    that the user account is active and not deactivated.
    
    Args:
        f (function): Function to decorate
        
    Returns:
        function: Decorated function with active user requirement
        
    Usage:
        @require_active_user
        def sensitive_operation():
            # Only active users can access this
            pass
            
    Note:
        - Automatically calls verify_jwt_in_request()
        - Checks user existence and active status
        - Returns 401 for any authentication failure
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            
            # Get current user (includes user_id conversion and database lookup)
            current_user = get_current_user()
            if not current_user:
                return jsonify({"error": "User not found"}), 401
            
            # Explicitly check account is active
            if not current_user.is_active:
                return jsonify({"error": "Account is deactivated"}), 401
            
            # User is authenticated and active - proceed
            return f(*args, **kwargs)
        except Exception as e:
            # Any authentication error results in 401
            return jsonify({"error": f"Authentication required: {str(e)}"}), 401
    
    return decorated_function

def admin_required(f):
    """
    Decorator for admin-only routes (placeholder for future admin functionality)
    
    This is a template for implementing admin-level access control.
    Currently allows all authenticated users but can be extended.
    
    Args:
        f (function): Function to decorate
        
    Returns:
        function: Decorated function with admin requirement
        
    Usage:
        @admin_required
        def admin_panel():
            # Only admins can access this
            pass
            
    TODO:
        - Add is_admin field to User model
        - Implement admin role checking logic
        - Add admin assignment functionality
    """
    @wraps(f)
    @jwt_required()  # Use Flask-JWT-Extended decorator for simplicity
    def decorated_function(*args, **kwargs):
        # Get current authenticated user
        current_user = get_current_user()
        if not current_user:
            return jsonify({"error": "User not found"}), 401
        
        # PLACEHOLDER: Add admin check when User model has is_admin field
        # if not current_user.is_admin:
        #     return jsonify({"error": "Admin access required"}), 403
        
        # Currently allows all authenticated users
        return f(*args, **kwargs)
    
    return decorated_function

def validate_token_manual(token):
    """
    Manual token validation function (alternative to Flask-JWT-Extended)
    
    This function provides an alternative way to validate JWT tokens
    without using Flask-JWT-Extended decorators.
    
    Args:
        token (str): JWT token string (may include 'Bearer ' prefix)
        
    Returns:
        tuple: (user: User or None, error: str or None)
        
    Usage:
        user, error = validate_token_manual(request.headers.get('Authorization'))
        if error:
            return jsonify({"error": error}), 401
            
    Note:
        - Handles 'Bearer ' prefix removal
        - Uses PyJWT library directly for validation
        - Returns user object and error for flexible handling
        - Useful for custom authentication flows
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]  # Remove first 7 characters
        
        # Decode and validate JWT token using PyJWT
        payload = pyjwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],  # Secret key for verification
            algorithms=['HS256']                   # Allowed algorithms (security)
        )
        
        # Extract user ID from token subject
        user_id = payload.get('sub')
        if not user_id:
            return None, "Invalid token: no user identity"
        
        # Look up user in database
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return None, "User not found"
        
        # Check account status
        if not user.is_active:
            return None, "Account is deactivated"
        
        # Validation successful
        return user, None
        
    except pyjwt.ExpiredSignatureError:
        # Token has passed its expiration time
        return None, "Token has expired"
    except pyjwt.InvalidTokenError:
        # Token is malformed, has wrong signature, etc.
        return None, "Invalid token"
    except Exception as e:
        # Catch-all for unexpected errors
        return None, f"Token validation error: {str(e)}"

def auth_middleware_manual(f):
    """
    Manual authentication middleware (alternative approach to auth_required)
    
    This decorator provides an alternative authentication method that doesn't
    rely on Flask-JWT-Extended's request context management.
    
    Args:
        f (function): Function to decorate
        
    Returns:
        function: Decorated function with manual authentication
        
    Usage:
        @auth_middleware_manual
        def custom_protected_route():
            # Access user via request.current_user
            user = request.current_user
            
    Note:
        - Uses manual token validation instead of Flask-JWT-Extended
        - Adds user to request context for route access
        - Useful for custom authentication requirements
        - Returns 401 for any authentication failure
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract Authorization header from request
        auth_header = request.headers.get('Authorization')
        
        # Check if Authorization header is present
        if not auth_header:
            return jsonify({"error": "Authorization header required"}), 401
        
        # Validate token and get user
        user, error = validate_token_manual(auth_header)
        if error:
            return jsonify({"error": error}), 401
        
        # Add user to request context for route access
        request.current_user = user
        
        # Proceed to route with authenticated user
        return f(*args, **kwargs)
    
    return decorated_function
