from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from models.user import db

class Trip(db.Model):
    """
    Trip model for storing user travel plans and itineraries
    
    This model represents a travel trip with destination, dates, location data,
    and detailed itinerary information. Each trip belongs to a specific user
    and includes metadata for tracking and management.
    """
    __tablename__ = 'trips'  # Explicit table name in database
    
    # PRIMARY KEY AND RELATIONSHIPS
    id = db.Column(db.Integer, primary_key=True)  # Unique trip identifier
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign key to users table
    
    # TRIP BASIC INFORMATION
    destination = db.Column(db.String(255), nullable=False)  # Trip destination (city, country, etc.)
    start_date = db.Column(db.Date, nullable=False)  # Trip start date (date only, no time)
    end_date = db.Column(db.Date, nullable=False)  # Trip end date (date only, no time)
    
    # LOCATION DATA (OPTIONAL)
    latitude = db.Column(db.Float, nullable=True)  # Geographic latitude coordinate
    longitude = db.Column(db.Float, nullable=True)  # Geographic longitude coordinate
    
    # DETAILED TRIP INFORMATION
    itinerary = db.Column(db.Text, nullable=True)  # JSON string containing day-by-day itinerary details
    
    # METADATA AND TIMESTAMPS
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Trip creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Auto-update on changes
    
    # RELATIONSHIPS
    # Define relationship with User model for easy access to user data
    # backref creates a 'trips' attribute on User instances to access all their trips
    user = db.relationship('User', backref=db.backref('trips', lazy=True))
    
    def __repr__(self):
        """String representation for debugging and logging"""
        return f'<Trip {self.destination} - {self.start_date} to {self.end_date}>'
    
    def to_dict(self):
        """
        Convert trip instance to dictionary for API responses
        
        Returns:
            dict: Trip data formatted for JSON API responses
            
        Note:
            - Converts dates to ISO format strings for JSON compatibility
            - Groups coordinates into nested object for cleaner API
            - Includes all relevant trip information
            - Safe for external API consumption
        """
        return {
            # Basic trip identification
            'id': self.id,
            'user_id': self.user_id,
            
            # Trip details
            'destination': self.destination,
            'start_date': self.start_date.isoformat() if self.start_date else None,  # Convert date to string
            'end_date': self.end_date.isoformat() if self.end_date else None,  # Convert date to string
            
            # Location data (grouped for cleaner API response)
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.latitude and self.longitude else None,  # Only include if both coordinates exist
            
            # Detailed information
            'itinerary': self.itinerary,  # JSON string (will be parsed by frontend)
            
            # Metadata
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO string
            'updated_at': self.updated_at.isoformat()   # Convert datetime to ISO string
        }
