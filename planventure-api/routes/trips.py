from flask import Blueprint, request, jsonify
from datetime import datetime, date
from utils.middleware import auth_required, get_current_user
from models.user import db
from models.trip import Trip
import json

trips_bp = Blueprint('trips', __name__, url_prefix='/trips')

def validate_trip_data(data, is_update=False):
    """Validate trip data for creation or update"""
    errors = []
    
    if not is_update or 'destination' in data:
        destination = data.get('destination', '').strip()
        if not destination:
            errors.append("Destination is required")
        elif len(destination) < 2:
            errors.append("Destination must be at least 2 characters long")
        elif len(destination) > 255:
            errors.append("Destination must be less than 255 characters")
    
    if not is_update or 'start_date' in data:
        start_date_str = data.get('start_date')
        if not start_date_str:
            errors.append("Start date is required")
        else:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                if start_date < date.today():
                    errors.append("Start date cannot be in the past")
            except ValueError:
                errors.append("Start date must be in YYYY-MM-DD format")
    
    if not is_update or 'end_date' in data:
        end_date_str = data.get('end_date')
        if not end_date_str:
            errors.append("End date is required")
        else:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if 'start_date' in data:
                    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                    if end_date <= start_date:
                        errors.append("End date must be after start date")
            except ValueError:
                errors.append("End date must be in YYYY-MM-DD format")
    
    # Validate coordinates (optional)
    if 'latitude' in data:
        try:
            lat = float(data['latitude'])
            if not -90 <= lat <= 90:
                errors.append("Latitude must be between -90 and 90")
        except (ValueError, TypeError):
            errors.append("Latitude must be a valid number")
    
    if 'longitude' in data:
        try:
            lng = float(data['longitude'])
            if not -180 <= lng <= 180:
                errors.append("Longitude must be between -180 and 180")
        except (ValueError, TypeError):
            errors.append("Longitude must be a valid number")
    
    # Validate itinerary (optional JSON)
    if 'itinerary' in data and data['itinerary']:
        try:
            if isinstance(data['itinerary'], str):
                json.loads(data['itinerary'])
        except json.JSONDecodeError:
            errors.append("Itinerary must be valid JSON")
    
    return errors

@trips_bp.route('', methods=['POST'])
@auth_required()
def create_trip():
    """Create a new trip for the authenticated user"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate trip data
    errors = validate_trip_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    try:
        # Create new trip
        new_trip = Trip(
            user_id=current_user.user_id,
            destination=data['destination'].strip(),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            latitude=float(data['latitude']) if data.get('latitude') else None,
            longitude=float(data['longitude']) if data.get('longitude') else None,
            itinerary=json.dumps(data['itinerary']) if data.get('itinerary') else None
        )
        
        db.session.add(new_trip)
        db.session.commit()
        
        return jsonify({
            "message": "Trip created successfully",
            "trip": new_trip.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create trip: {str(e)}"}), 500

@trips_bp.route('', methods=['GET'])
@auth_required()
def get_user_trips():
    """Get all trips for the authenticated user"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Get query parameters for pagination and filtering
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page
        
        # Optional filtering
        destination_filter = request.args.get('destination')
        
        # Build query
        query = Trip.query.filter_by(user_id=current_user.user_id)
        
        if destination_filter:
            query = query.filter(Trip.destination.ilike(f'%{destination_filter}%'))
        
        # Order by creation date (newest first)
        query = query.order_by(Trip.created_at.desc())
        
        # Paginate
        trips = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
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
@auth_required()
def get_trip(trip_id):
    """Get a specific trip by ID"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        return jsonify({
            "trip": trip.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve trip: {str(e)}"}), 500

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@auth_required()
def update_trip(trip_id):
    """Update a specific trip"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        # Validate update data
        errors = validate_trip_data(data, is_update=True)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        # Update trip fields
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
        
        # Update timestamp
        trip.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "message": "Trip updated successfully",
            "trip": trip.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update trip: {str(e)}"}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@auth_required()
def delete_trip(trip_id):
    """Delete a specific trip"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user.user_id).first()
        
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        # Store trip info for response
        trip_info = {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat()
        }
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({
            "message": "Trip deleted successfully",
            "deleted_trip": trip_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete trip: {str(e)}"}), 500

@trips_bp.route('/search', methods=['GET'])
@auth_required()
def search_trips():
    """Search trips by various criteria"""
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 401
    
    try:
        # Get search parameters
        destination = request.args.get('destination')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Trip.query.filter_by(user_id=current_user.user_id)
        
        if destination:
            query = query.filter(Trip.destination.ilike(f'%{destination}%'))
        
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Trip.start_date >= start_dt)
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Trip.end_date <= end_dt)
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        trips = query.order_by(Trip.created_at.desc()).all()
        
        return jsonify({
            "trips": [trip.to_dict() for trip in trips],
            "total": len(trips)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500
