from flask import Blueprint, jsonify, request
from utils.middleware import auth_required, get_current_user, require_active_user
from flask_jwt_extended import get_jwt_identity

# Create blueprint for protected routes
protected_bp = Blueprint('protected', __name__, url_prefix='/api')

@protected_bp.route('/profile', methods=['GET'])
@auth_required()
def get_profile():
    """Get current user's profile - requires authentication"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    return jsonify({
        "message": "Profile retrieved successfully",
        "user": current_user.get_user_info()
    }), 200

@protected_bp.route('/profile', methods=['PUT'])
@require_active_user
def update_profile():
    """Update user profile - requires active user"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({"error": "User not found"}), 401
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Example profile update logic
    if 'email' in data:
        return jsonify({"error": "Email cannot be changed via this endpoint"}), 400
    
    return jsonify({
        "message": "Profile update endpoint ready",
        "user_id": current_user.user_id
    }), 200

@protected_bp.route('/public-data', methods=['GET'])
@auth_required(optional=True)
def get_public_data():
    """Public endpoint that provides extra info if user is authenticated"""
    current_user = get_current_user()
    
    base_data = {
        "public_message": "This is public data available to everyone",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    if current_user:
        base_data["authenticated_user"] = current_user.email_address
        base_data["extra_info"] = "This extra info is only shown to authenticated users"
    
    return jsonify(base_data), 200

@protected_bp.route('/user-only', methods=['GET'])
@auth_required()
def user_only_endpoint():
    """Example endpoint that requires authentication"""
    user_id = get_jwt_identity()
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    return jsonify({
        "message": "This endpoint requires authentication",
        "user_id": user_id,
        "email": current_user.email_address
    }), 200

@protected_bp.route('/test-auth', methods=['GET'])
@auth_required()
def test_auth_required():
    """Test route that requires authentication"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    return jsonify({
        "message": "Authentication test successful!",
        "user_id": current_user.user_id,
        "email": current_user.email_address,
        "test_type": "auth_required"
    }), 200

@protected_bp.route('/test-auth-optional', methods=['GET'])
@auth_required(optional=True)
def test_auth_optional():
    """Test route with optional authentication"""
    current_user = get_current_user()
    
    response_data = {
        "message": "Optional auth test successful!",
        "test_type": "auth_optional",
        "public_data": "This is available to everyone"
    }
    
    if current_user:
        response_data["authenticated_user"] = current_user.email_address
        response_data["user_id"] = current_user.user_id
        response_data["private_data"] = "This extra data is only for authenticated users"
    else:
        response_data["auth_status"] = "No authentication provided"
    
    return jsonify(response_data), 200

@protected_bp.route('/test-no-auth', methods=['GET'])
def test_no_auth():
    """Test route that requires no authentication"""
    return jsonify({
        "message": "No authentication required test successful!",
        "test_type": "no_auth_required",
        "public_info": "This endpoint is completely public"
    }), 200
