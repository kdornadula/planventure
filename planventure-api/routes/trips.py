from flask import Blueprint, request, jsonify
from datetime import datetime, date
from utils.middleware import auth_required, get_current_user
from models.user import db
from models.trip import Trip
import json
from utils.itinerary_templates import (
    generate_default_itinerary,
    generate_weekend_getaway_template,
    generate_business_trip_template,
    get_city_specific_suggestions
)

# Create blueprint for trip-related routes
# All routes will be prefixed with '/trips'
trips_bp = Blueprint('trips', __name__, url_prefix='/trips')

def validate_trip_data(data, is_update=False):
    """
    Validate trip data for creation or update operations
    
    Args:
        data (dict): Trip data from request JSON
        is_update (bool): If True, allows partial data (for updates)
                         If False, requires all fields (for creation)
                         
    Returns:
        list: List of validation error messages (empty if valid)
        
    Note:
        - Validates destination, dates, coordinates, and itinerary
        - For updates, only validates fields that are present
        - Returns detailed error messages for user feedback
        - Used by both create and update endpoints
    """
    errors = []
    
    # DESTINATION VALIDATION
    # Only validate destination if creating new trip or field is being updated
    if not is_update or 'destination' in data:
        destination = data.get('destination', '').strip()
        if not destination:
            errors.append("Destination is required")
        elif len(destination) < 2:
            errors.append("Destination must be at least 2 characters long")
        elif len(destination) > 255:
            errors.append("Destination must be less than 255 characters")
    
    # START DATE VALIDATION
    if not is_update or 'start_date' in data:
        start_date_str = data.get('start_date')
        if not start_date_str:
            errors.append("Start date is required")
        else:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # Prevent scheduling trips in the past
                if start_date < date.today():
                    errors.append("Start date cannot be in the past")
            except ValueError:
                errors.append("Start date must be in YYYY-MM-DD format")
    
    # END DATE VALIDATION
    if not is_update or 'end_date' in data:
        end_date_str = data.get('end_date')
        if not end_date_str:
            errors.append("End date is required")
        else:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                # Ensure end date is after start date (if start date is also being set)
                if 'start_date' in data:
                    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                    if end_date <= start_date:
                        errors.append("End date must be after start date")
            except ValueError:
                errors.append("End date must be in YYYY-MM-DD format")
    
    # COORDINATE VALIDATION (OPTIONAL FIELDS)
    # Validate latitude if provided
    if 'latitude' in data:
        try:
            lat = float(data['latitude'])
            if not -90 <= lat <= 90:
                errors.append("Latitude must be between -90 and 90")
        except (ValueError, TypeError):
            errors.append("Latitude must be a valid number")
    
    # Validate longitude if provided
    if 'longitude' in data:
        try:
            lng = float(data['longitude'])
            if not -180 <= lng <= 180:
                errors.append("Longitude must be between -180 and 180")
        except (ValueError, TypeError):
            errors.append("Longitude must be a valid number")
    
    # ITINERARY VALIDATION (OPTIONAL JSON FIELD)
    if 'itinerary' in data and data['itinerary']:
        try:
            # If itinerary is provided as string, validate it's valid JSON
            if isinstance(data['itinerary'], str):
                json.loads(data['itinerary'])
            # If it's already a dict/object, it should be fine
        except json.JSONDecodeError:
            errors.append("Itinerary must be valid JSON")
    
    return errors

# CRUD OPERATIONS FOR TRIPS

@trips_bp.route('', methods=['POST'])
@auth_required()  # Requires valid JWT token
def create_trip():
    """
    Create a new trip for the authenticated user
    
    Expected JSON payload:
        {
            "destination": "Paris, France",
            "start_date": "2024-06-01",
            "end_date": "2024-06-07",
            "latitude": 48.8566,          // optional
            "longitude": 2.3522,          // optional
            "itinerary": {...}            // optional JSON object
        }
        
    Returns:
        201: Trip created successfully
        400: Invalid input data
        401: Not authenticated
        500: Server error
        
    Note:
        - Only authenticated users can create trips
        - Trip is automatically associated with current user
        - Validates all input data before saving
        - Returns complete trip data with auto-generated ID
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    # Extract and validate request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate trip data (all fields required for creation)
    errors = validate_trip_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    try:
        # Create new trip instance
        new_trip = Trip(
            user_id=current_user.user_id,  # Associate with current user
            destination=data['destination'].strip(),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            # Optional fields - use None if not provided
            latitude=float(data['latitude']) if data.get('latitude') else None,
            longitude=float(data['longitude']) if data.get('longitude') else None,
            # Store itinerary as JSON string
            itinerary=json.dumps(data['itinerary']) if data.get('itinerary') else None
        )
        
        # Save to database with transaction safety
        db.session.add(new_trip)
        db.session.commit()
        
        # Return success response with complete trip data
        return jsonify({
            "message": "Trip created successfully",
            "trip": new_trip.to_dict()  # Includes auto-generated ID and timestamps
        }), 201
        
    except Exception as e:
        # Rollback database changes on error
        db.session.rollback()
        return jsonify({"error": f"Failed to create trip: {str(e)}"}), 500

@trips_bp.route('', methods=['GET'])
@auth_required()  # Requires valid JWT token
def get_user_trips():
    """
    Get all trips for the authenticated user with pagination and filtering
    
    Query parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10, max: 100)
        destination (str): Filter by destination (partial match)
        
    Returns:
        200: List of trips with pagination info
        401: Not authenticated
        500: Server error
        
    Note:
        - Only returns trips belonging to current user
        - Supports pagination to handle large trip lists
        - Supports filtering by destination
        - Orders by creation date (newest first)
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Extract pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Cap at 100 for performance
        
        # Extract optional filtering parameters
        destination_filter = request.args.get('destination')
        
        # Build query - start with user's trips only
        query = Trip.query.filter_by(user_id=current_user.user_id)
        
        # Apply destination filter if provided (case-insensitive partial match)
        if destination_filter:
            query = query.filter(Trip.destination.ilike(f'%{destination_filter}%'))
        
        # Order by creation date (newest trips first)
        query = query.order_by(Trip.created_at.desc())
        
        # Apply pagination
        trips = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False  # Don't raise error for invalid page numbers
        )
        
        # Return trips with pagination metadata
        return jsonify({
            "trips": [trip.to_dict() for trip in trips.items],
            "pagination": {
                "page": page,
                "pages": trips.pages,
                "per_page": per_page,
                "total": trips.total,
                "has_next": trips.has_next,
                "has_prev": trips.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve trips: {str(e)}"}), 500

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@auth_required()  # Requires valid JWT token
def get_trip(trip_id):
    """
    Get a specific trip by ID (user can only access their own trips)
    
    Args:
        trip_id (int): ID of the trip to retrieve
        
    Returns:
        200: Trip data
        401: Not authenticated
        404: Trip not found or not owned by user
        500: Server error
        
    Note:
        - Only returns trip if it belongs to current user
        - Prevents users from accessing other users' trips
        - Returns complete trip data including itinerary
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Look up trip by ID AND user_id (ensures user owns this trip)
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        # Return 404 if trip doesn't exist or doesn't belong to user
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        # Return complete trip data
        return jsonify({
            "trip": trip.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve trip: {str(e)}"}), 500

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@auth_required()  # Requires valid JWT token
def update_trip(trip_id):
    """
    Update a specific trip (partial updates supported)
    
    Args:
        trip_id (int): ID of the trip to update
        
    Expected JSON payload (all fields optional for updates):
        {
            "destination": "Updated destination",
            "start_date": "2024-07-01",
            "end_date": "2024-07-07",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "itinerary": {...}
        }
        
    Returns:
        200: Trip updated successfully
        400: Invalid input data
        401: Not authenticated
        404: Trip not found or not owned by user
        500: Server error
        
    Note:
        - Supports partial updates (only provided fields are updated)
        - Validates all provided data
        - Updates timestamp automatically
        - Only allows users to update their own trips
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    # Extract and validate request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Look up trip by ID AND user_id (ensures user owns this trip)
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        # Return 404 if trip doesn't exist or doesn't belong to user
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        # Validate update data (only validates provided fields)
        errors = validate_trip_data(data, is_update=True)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        # Update only the fields that were provided
        if 'destination' in data:
            trip.destination = data['destination'].strip()
        
        if 'start_date' in data:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        
        if 'end_date' in data:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if 'latitude' in data:
            trip.latitude = float(data['latitude']) if data['latitude'] else None
        
        if 'longitude' in data:
            trip.longitude = float(data['longitude']) if data['longitude'] else None
        
        if 'itinerary' in data:
            trip.itinerary = json.dumps(data['itinerary']) if data['itinerary'] else None
        
        # Update timestamp (SQLAlchemy also does this automatically)
        trip.updated_at = datetime.utcnow()
        
        # Save changes to database
        db.session.commit()
        
        # Return updated trip data
        return jsonify({
            "message": "Trip updated successfully",
            "trip": trip.to_dict()
        }), 200
        
    except Exception as e:
        # Rollback database changes on error
        db.session.rollback()
        return jsonify({"error": f"Failed to update trip: {str(e)}"}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@auth_required()  # Requires valid JWT token
def delete_trip(trip_id):
    """
    Delete a specific trip
    
    Args:
        trip_id (int): ID of the trip to delete
        
    Returns:
        200: Trip deleted successfully
        401: Not authenticated
        404: Trip not found or not owned by user
        500: Server error
        
    Note:
        - Only allows users to delete their own trips
        - Permanently removes trip from database
        - Returns basic trip info for confirmation
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Look up trip by ID AND user_id (ensures user owns this trip)
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        # Return 404 if trip doesn't exist or doesn't belong to user
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        # Store trip info for confirmation response (before deletion)
        trip_info = {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat()
        }
        
        # Delete trip from database
        db.session.delete(trip)
        db.session.commit()
        
        # Return confirmation
        return jsonify({
            "message": "Trip deleted successfully",
            "deleted_trip": trip_info
        }), 200
        
    except Exception as e:
        # Rollback database changes on error
        db.session.rollback()
        return jsonify({"error": f"Failed to delete trip: {str(e)}"}), 500

# SEARCH AND TEMPLATE OPERATIONS

@trips_bp.route('/search', methods=['GET'])
@auth_required()  # Requires valid JWT token
def search_trips():
    """
    Search trips by various criteria
    
    Query parameters:
        destination (str): Filter by destination (partial match)
        start_date (str): Find trips starting on or after this date (YYYY-MM-DD)
        end_date (str): Find trips ending on or before this date (YYYY-MM-DD)
        
    Returns:
        200: List of matching trips
        400: Invalid date format
        401: Not authenticated
        500: Server error
        
    Note:
        - Only searches within current user's trips
        - Supports multiple filter criteria simultaneously
        - Returns trips ordered by creation date (newest first)
    """
    # Get current authenticated user
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Extract search parameters from query string
        destination = request.args.get('destination')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query - start with user's trips only
        query = Trip.query.filter_by(user_id=current_user.user_id)
        
        # Apply destination filter (case-insensitive partial match)
        if destination:
            query = query.filter(Trip.destination.ilike(f'%{destination}%'))
        
        # Apply start date filter (trips starting on or after this date)
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Trip.start_date >= start_dt)
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
        
        # Apply end date filter (trips ending on or before this date)
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Trip.end_date <= end_dt)
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        # Execute query and order results
        trips = query.order_by(Trip.created_at.desc()).all()
        
        # Return search results
        return jsonify({
            "trips": [trip.to_dict() for trip in trips],
            "total": len(trips)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@trips_bp.route('/template', methods=['GET'])
@auth_required()
def get_itinerary_template():
    """Generate a default itinerary template"""
    destination = request.args.get('destination')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    trip_type = request.args.get('trip_type', 'leisure')
    
    if not all([destination, start_date, end_date]):
        return jsonify({
            "error": "Missing required parameters",
            "required": ["destination", "start_date", "end_date"],
            "optional": ["trip_type"]
        }), 400
    
    try:
        template = generate_default_itinerary(destination, start_date, end_date, trip_type)
        
        return jsonify({
            "message": "Itinerary template generated successfully",
            "template": template
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to generate template: {str(e)}"}), 500

@trips_bp.route('/template/weekend', methods=['GET'])
@auth_required()
def get_weekend_template():
    """Generate a weekend getaway template"""
    destination = request.args.get('destination')
    
    if not destination:
        return jsonify({"error": "Destination parameter required"}), 400
    
    try:
        template = generate_weekend_getaway_template(destination)
        
        return jsonify({
            "message": "Weekend template generated successfully",
            "template": template
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate weekend template: {str(e)}"}), 500

@trips_bp.route('/template/business', methods=['GET'])
@auth_required()
def get_business_template():
    """Generate a business trip template"""
    destination = request.args.get('destination')
    duration = request.args.get('duration', 3, type=int)
    
    if not destination:
        return jsonify({"error": "Destination parameter required"}), 400
    
    try:
        template = generate_business_trip_template(destination, duration)
        
        return jsonify({
            "message": "Business trip template generated successfully",
            "template": template
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate business template: {str(e)}"}), 500

@trips_bp.route('/suggestions/<destination>', methods=['GET'])
@auth_required()
def get_destination_suggestions(destination):
    """Get activity suggestions for a specific destination"""
    try:
        suggestions = get_city_specific_suggestions(destination)
        
        return jsonify({
            "destination": destination,
            "suggestions": suggestions,
            "count": len(suggestions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get suggestions: {str(e)}"}), 500
