from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.user import User, db
import jwt as pyjwt

def auth_required(optional=False):
    """
    Decorator to protect routes with JWT authentication
    
    Args:
        optional (bool): If True, allows access without token but provides user context if token exists
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                print(f"🔍 Debug - auth_required called, optional={optional}")
                
                if optional:
                    # Optional authentication - don't fail if no token
                    verify_jwt_in_request(optional=True)
                    current_user_id = get_jwt_identity()
                    print(f"🔍 Debug - optional auth, user_id: {current_user_id} (type: {type(current_user_id)})")
                    if current_user_id:
                        # Convert to int if it's a string
                        if isinstance(current_user_id, str):
                            try:
                                current_user_id = int(current_user_id)
                            except ValueError:
                                print(f"❌ Could not convert user_id to int: {current_user_id}")
                                return f(*args, **kwargs)  # Continue without auth for optional
                        
                        user = User.query.filter_by(user_id=current_user_id).first()
                        if user and not user.is_active:
                            return jsonify({"error": "User account is inactive"}), 401
                else:
                    # Required authentication
                    print("🔍 Debug - verifying JWT...")
                    verify_jwt_in_request()
                    current_user_id = get_jwt_identity()
                    print(f"🔍 Debug - required auth, user_id: {current_user_id} (type: {type(current_user_id)})")
                    
                    if not current_user_id:
                        return jsonify({"error": "Invalid token: no user identity"}), 401
                    
                    # Convert to int if it's a string
                    if isinstance(current_user_id, str):
                        try:
                            current_user_id = int(current_user_id)
                        except ValueError:
                            return jsonify({"error": "Invalid user ID format"}), 401
                    
                    user = User.query.filter_by(user_id=current_user_id).first()
                    print(f"🔍 Debug - found user: {user}")
                    
                    if not user:
                        return jsonify({"error": "User not found"}), 401
                    
                    if not user.is_active:
                        return jsonify({"error": "Account is deactivated"}), 401
                
                print("🔍 Debug - authentication successful, calling route")
                return f(*args, **kwargs)
                
            except Exception as e:
                print(f"❌ Debug - Exception in auth_required: {e}")
                print(f"❌ Debug - Exception type: {type(e)}")
                if optional:
                    return f(*args, **kwargs)
                return jsonify({"error": f"Authentication failed: {str(e)}"}), 401
                
        return decorated_function
    return decorator

def get_current_user():
    """
    Get the current authenticated user from JWT token
    
    Returns:
        User object if authenticated, None otherwise
    """
    try:
        current_user_id = get_jwt_identity()
        print(f"🔍 Debug - current_user_id from token: {current_user_id} (type: {type(current_user_id)})")
        
        if current_user_id:
            # Convert string user_id to integer for database lookup
            if isinstance(current_user_id, str):
                try:
                    current_user_id = int(current_user_id)
                except ValueError:
                    print(f"❌ Could not convert user_id to int: {current_user_id}")
                    return None
            
            user = User.query.filter_by(user_id=current_user_id).first()
            print(f"🔍 Debug - found user: {user}")
            return user
    except Exception as e:
        print(f"❌ Error getting current user: {e}")
    return None

def require_active_user(f):
    """
    Decorator that requires an active user account
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_current_user()
            if not current_user:
                return jsonify({"error": "User not found"}), 401
            
            if not current_user.is_active:
                return jsonify({"error": "Account is deactivated"}), 401
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": f"Authentication required: {str(e)}"}), 401
    
    return decorated_function

def admin_required(f):
    """
    Decorator for admin-only routes (placeholder for future admin functionality)
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({"error": "User not found"}), 401
        
        # Placeholder for admin check - you can add admin field to User model later
        # if not current_user.is_admin:
        #     return jsonify({"error": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def validate_token_manual(token):
    """
    Manual token validation function (alternative to Flask-JWT-Extended)
    """
    try:
        if token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer ' prefix
        
        payload = pyjwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        
        user_id = payload.get('sub')
        if not user_id:
            return None, "Invalid token: no user identity"
        
        # FIX: use filter_by instead of get
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return None, "User not found"
        
        if not user.is_active:
            return None, "Account is deactivated"
        
        return user, None
        
    except pyjwt.ExpiredSignatureError:
        return None, "Token has expired"
    except pyjwt.InvalidTokenError:
        return None, "Invalid token"
    except Exception as e:
        return None, f"Token validation error: {str(e)}"

def auth_middleware_manual(f):
    """
    Manual authentication middleware (alternative approach)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header required"}), 401
        
        user, error = validate_token_manual(auth_header)
        if error:
            return jsonify({"error": error}), 401
        
        # Add user to request context
        request.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function
