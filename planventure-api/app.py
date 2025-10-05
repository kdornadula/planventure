import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models.user import db
from models.trip import Trip  # Import to ensure table creation
from sqlalchemy import text

# Load environment variables from .env file for secure configuration
load_dotenv()

# Initialize Flask application instance
app = Flask(__name__)

# CONFIGURATION SECTION
# Set up application configuration from environment variables with fallback defaults
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')  # Used for Flask sessions and security
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # Used for JWT token signing
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')  # Database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system (saves memory)

# EXTENSIONS INITIALIZATION
# Initialize Flask extensions with the app instance
db.init_app(app)  # Database ORM
jwt = JWTManager(app)  # JWT token management

# Enhanced CORS configuration for React frontend
CORS(app, 
     origins=os.getenv('CORS_ORIGINS', 'https://kdornadula.github.io,http://localhost:3000').split(','),
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# JWT ERROR HANDLERS
# Custom error handlers for different JWT-related failures
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle requests with expired JWT tokens"""
    return jsonify({"error": "Token has expired", "message": "Please log in again"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle requests with malformed or invalid JWT tokens"""
    return jsonify({"error": "Invalid token", "message": "Token is invalid or malformed"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle requests missing required JWT tokens"""
    return jsonify({"error": "Token required", "message": "Request does not contain an access token"}), 401

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    """Add additional claims to JWT tokens (user_id for convenience)"""
    return {"user_id": identity}

# BASIC ROUTES
# Core application routes for health checking and basic information
@app.route('/')
def home():
    """Welcome endpoint - provides basic API information"""
    return jsonify({"message": "Welcome to PlanVenture API"})

# ENHANCED HEALTH CHECK ENDPOINTS
@app.route('/health')
def health_check():
    """
    Enhanced health check endpoint with database connectivity and system status
    
    Returns:
        200: System healthy with detailed status
        503: System unhealthy with error details
        
    Note:
        - Checks database connectivity
        - Validates essential environment variables
        - Used for monitoring, load balancers, and deployment verification
    """
    try:
        # Test database connectivity - fix the SQL syntax
        db.session.execute(text('SELECT 1'))
        db_status = "connected"
        db_healthy = True
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_healthy = False
    
    # Check essential environment variables
    env_checks = {
        "SECRET_KEY": bool(os.getenv('SECRET_KEY')),
        "JWT_SECRET_KEY": bool(os.getenv('JWT_SECRET_KEY')),
        "DATABASE_URL": bool(os.getenv('DATABASE_URL'))
    }
    
    # Overall health status
    overall_healthy = db_healthy and all(env_checks.values())
    
    health_data = {
        "status": "healthy" if overall_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": {
            "status": db_status,
            "healthy": db_healthy
        },
        "environment": {
            "variables_configured": env_checks,
            "cors_origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
        },
        "services": {
            "authentication": "operational",
            "trip_management": "operational",
            "templates": "operational"
        }
    }
    
    # Return appropriate status code
    status_code = 200 if overall_healthy else 503
    return jsonify(health_data), status_code

@app.route('/health/simple')
def simple_health_check():
    """Simple health check for basic monitoring"""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()}), 200

@app.route('/health/database')
def database_health_check():
    """Specific database connectivity check"""
    try:
        # Test database with a simple query - fix syntax here too
        result = db.session.execute(text('SELECT COUNT(*) FROM users'))
        user_count = result.scalar()
        
        return jsonify({
            "database": "healthy",
            "user_count": user_count,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "database": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503

# BLUEPRINT REGISTRATION
# Register route blueprints (modular route collections) with error handling
try:
    # Authentication routes (register, login, email validation)
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    print("✅ Auth routes registered successfully")
    
    # Protected example routes (for testing authentication middleware)
    from routes.protected_example import protected_bp
    app.register_blueprint(protected_bp)
    print("✅ Protected routes registered successfully")
    
    # Trip management routes (CRUD operations for trips)
    from routes.trips import trips_bp
    app.register_blueprint(trips_bp)
    print("✅ Trips routes registered successfully")
    
except ImportError as e:
    # Handle cases where blueprint imports fail (missing dependencies, syntax errors)
    print(f"❌ Warning: Could not import routes: {e}")

# DEBUGGING UTILITIES
@app.route('/routes')
def list_routes():
    """Development endpoint - lists all available routes for debugging"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,  # Function name
            'methods': list(rule.methods),  # HTTP methods (GET, POST, etc.)
            'path': str(rule)  # URL pattern
        })
    return jsonify(routes)

# DATABASE INITIALIZATION
def create_tables():
    """Initialize database tables within Flask application context"""
    with app.app_context():
        db.create_all()  # Create all tables defined in models

# APPLICATION ENTRY POINT
if __name__ == '__main__':
    # Only run when script is executed directly (not imported)
    create_tables()  # Ensure database tables exist
    app.run(debug=True)  # Start development server with debug mode enabled
