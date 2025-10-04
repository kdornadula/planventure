from datetime import datetime, timedelta
import json
from typing import Dict, Any, List

def generate_default_itinerary(destination, start_date_str, end_date_str, trip_type='leisure'):
    """
    Generate a default itinerary template based on destination and dates
    
    Args:
        destination (str): The travel destination
        start_date_str (str): Start date in YYYY-MM-DD format
        end_date_str (str): End date in YYYY-MM-DD format
        trip_type (str): Type of trip (leisure, business, adventure, cultural)
        
    Returns:
        dict: Complete itinerary template with day-by-day activities
        
    Raises:
        ValueError: If dates are invalid or end date is before start date
    """
    # Parse and validate the input dates
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")
    
    # Ensure end date is after start date
    if end_date <= start_date:
        raise ValueError("End date must be after start date")
    
    # Calculate the total trip duration in days
    duration = (end_date - start_date).days
    
    # Build the day-by-day itinerary
    itinerary = {}
    current_date = start_date
    
    # Generate activities for each day of the trip
    for day_num in range(duration):
        day_key = f"Day {day_num + 1} ({current_date.strftime('%Y-%m-%d')})"
        
        if day_num == 0:  # First day - arrival activities
            itinerary[day_key] = {
                "morning": "Arrival and hotel check-in",
                "afternoon": f"Explore {destination} city center",
                "evening": "Welcome dinner at local restaurant"
            }
        elif day_num == duration - 1:  # Last day - departure activities
            itinerary[day_key] = {
                "morning": "Final sightseeing and souvenir shopping",
                "afternoon": "Pack and prepare for departure",
                "evening": "Departure"
            }
        else:  # Middle days - regular activities based on trip type
            itinerary[day_key] = get_day_template(destination, day_num + 1, trip_type)
        
        # Move to next day
        current_date += timedelta(days=1)
    
    # Return comprehensive itinerary package
    return {
        "destination": destination,
        "trip_type": trip_type,
        "duration_days": duration,
        "itinerary": itinerary,
        "general_tips": get_destination_tips(destination),
        "packing_checklist": generate_packing_checklist(trip_type, duration)
    }

def get_day_template(destination, day_number, trip_type):
    """
    Get activity template for a specific day based on trip type
    
    Args:
        destination (str): The travel destination
        day_number (int): Day number in the trip
        trip_type (str): Type of trip (leisure, business, adventure, cultural)
        
    Returns:
        dict: Activities for morning, afternoon, and evening
    """
    # Pre-defined activity templates for different trip types
    templates = {
        'leisure': {
            "morning": f"Visit main attraction in {destination}",
            "afternoon": "Lunch and explore local neighborhoods", 
            "evening": "Dinner and local entertainment"
        },
        'business': {
            "morning": "Business meetings",
            "afternoon": "Lunch meeting and conference sessions",
            "evening": "Networking dinner"
        },
        'adventure': {
            "morning": f"Outdoor activity in {destination}",
            "afternoon": "Adventure sports or hiking",
            "evening": "Rest and local cuisine"
        },
        'cultural': {
            "morning": f"Visit museums in {destination}",
            "afternoon": "Cultural sites and historical landmarks",
            "evening": "Local cultural show or performance"
        }
    }
    
    # Return template for specified trip type, default to leisure if not found
    return templates.get(trip_type, templates['leisure'])

def generate_packing_checklist(trip_type='leisure', duration=3):
    """
    Generate a packing checklist based on trip type and duration
    
    Args:
        trip_type (str): Type of trip (leisure, business, adventure)
        duration (int): Trip duration in days
        
    Returns:
        dict: Categorized packing checklist
    """
    # Base items that everyone needs regardless of trip type
    base_items = {
        "essentials": [
            "Passport/ID",
            "Travel insurance documents", 
            "Flight tickets",
            "Hotel confirmations"
        ],
        "clothing": [
            "Comfortable walking shoes",
            "Weather-appropriate clothing",
            "Undergarments",
            "Sleepwear"
        ],
        "toiletries": [
            "Toothbrush and toothpaste",
            "Shampoo/soap",
            "Medications",
            "Sunscreen"
        ],
        "electronics": [
            "Camera",
            "Power bank",
            "Travel adapter",
            "Phone/tablet"
        ]
    }
    
    # Add trip-type specific items
    if trip_type == "business":
        base_items["business"] = [
            "Business attire",
            "Laptop",
            "Business cards",
            "Presentation materials"
        ]
    elif trip_type == "adventure":
        base_items["adventure"] = [
            "Outdoor gear",
            "Sturdy hiking boots",
            "Weather-appropriate clothing",
            "First aid kit"
        ]
    
    # Add items for longer trips (more than a week)
    if duration > 7:
        base_items["extended_stay"] = [
            "Laundry supplies",
            "Extra medications",
            "Variety of clothing options"
        ]
    
    return base_items

def generate_weekend_getaway_template(destination):
    """
    Generate a specialized template for weekend trips (2-3 days)
    
    Args:
        destination (str): The travel destination
        
    Returns:
        dict: Weekend-specific itinerary template with quick tips
    """
    return {
        "template_type": "Weekend Getaway",
        "destination": destination,
        "duration": "2 days",
        "itinerary": {
            # Saturday - main exploration day
            "Day 1 (Saturday)": {
                "morning": "Arrival and hotel check-in",
                "afternoon": f"Explore main attractions in {destination}",
                "evening": "Dinner at popular local restaurant"
            },
            # Sunday - leisurely wrap-up day
            "Day 2 (Sunday)": {
                "morning": "Visit local market or cultural site",
                "afternoon": "Leisure activities and shopping",
                "evening": "Departure"
            }
        },
        # Quick packing tips for short trips
        "packing_tips": ["Comfortable walking shoes", "Camera", "Light jacket"],
        # Budget estimation for weekend trips
        "budget_estimate": "Weekend budget: $200-500 per person"
    }

def generate_business_trip_template(destination, duration=3):
    """
    Generate a specialized template for business trips
    
    Args:
        destination (str): The business travel destination
        duration (int): Trip duration in days (default: 3)
        
    Returns:
        dict: Business-specific itinerary template with professional tips
    """
    itinerary = {}
    
    # Generate business-focused daily schedules
    for day in range(1, duration + 1):
        if day == 1:  # Arrival day
            itinerary[f"Day {day}"] = {
                "morning": "Arrival and hotel check-in",
                "afternoon": "Initial business meetings",
                "evening": "Welcome dinner with colleagues"
            }
        elif day == duration:  # Departure day
            itinerary[f"Day {day}"] = {
                "morning": "Final meetings and wrap-up",
                "afternoon": "Pack and prepare for departure",
                "evening": "Departure"
            }
        else:  # Full business days
            itinerary[f"Day {day}"] = {
                "morning": "Business conferences/meetings",
                "afternoon": "Lunch meetings and presentations",
                "evening": "Networking events"
            }
    
    return {
        "template_type": "Business Trip",
        "destination": destination,
        "duration": f"{duration} days",
        "itinerary": itinerary,
        # Essential items for business travelers
        "business_essentials": [
            "Business cards",
            "Laptop and chargers",
            "Professional attire",
            "Meeting materials"
        ],
        # Professional networking advice
        "networking_tips": [
            "Research attendees beforehand",
            "Prepare elevator pitch",
            "Follow up within 24 hours"
        ]
    }

def get_city_specific_suggestions(destination):
    """
    Get activity suggestions based on specific destination
    
    Args:
        destination (str): The travel destination
        
    Returns:
        list: List of suggested activities with categories and durations
    """
    # Database of popular activities for major cities
    # In a real application, this could be fetched from external APIs
    city_suggestions = {
        "paris": [
            {"activity": "Visit Eiffel Tower", "category": "sightseeing", "duration": "2-3 hours"},
            {"activity": "Louvre Museum", "category": "culture", "duration": "4-5 hours"},
            {"activity": "Seine River Cruise", "category": "leisure", "duration": "1-2 hours"},
            {"activity": "Montmartre District", "category": "sightseeing", "duration": "3-4 hours"},
            {"activity": "French Cooking Class", "category": "experience", "duration": "3 hours"}
        ],
        "london": [
            {"activity": "British Museum", "category": "culture", "duration": "3-4 hours"},
            {"activity": "Tower of London", "category": "history", "duration": "2-3 hours"},
            {"activity": "Thames River Walk", "category": "leisure", "duration": "1-2 hours"},
            {"activity": "West End Show", "category": "entertainment", "duration": "3 hours"},
            {"activity": "Afternoon Tea", "category": "experience", "duration": "2 hours"}
        ],
        "tokyo": [
            {"activity": "Senso-ji Temple", "category": "culture", "duration": "2 hours"},
            {"activity": "Shibuya Crossing", "category": "sightseeing", "duration": "1 hour"},
            {"activity": "Tsukiji Fish Market", "category": "experience", "duration": "2-3 hours"},
            {"activity": "Cherry Blossom Viewing", "category": "nature", "duration": "2-4 hours"},
            {"activity": "Ramen Tasting Tour", "category": "food", "duration": "3 hours"}
        ]
    }
    
    # Extract city name and normalize it (remove country, make lowercase)
    dest_key = destination.lower().split(',')[0].strip()
    
    # Return city-specific suggestions or generic ones if city not found
    return city_suggestions.get(dest_key, [
        {"activity": f"Explore {destination} city center", "category": "sightseeing", "duration": "2-3 hours"},
        {"activity": f"Visit {destination} main attractions", "category": "sightseeing", "duration": "3-4 hours"},
        {"activity": f"Try local cuisine in {destination}", "category": "food", "duration": "1-2 hours"},
        {"activity": f"Walk around {destination} neighborhoods", "category": "leisure", "duration": "2-3 hours"}
    ])

def get_destination_tips(destination):
    """
    Get general travel tips for any destination
    
    Args:
        destination (str): The travel destination
        
    Returns:
        list: List of general travel tips
    """
    # Universal travel tips that apply to most destinations
    return [
        f"Check weather forecast for {destination}",  # Weather-specific tip
        "Book accommodations in advance",              # Planning tip
        "Research local customs and etiquette",       # Cultural tip
        "Keep copies of important documents",         # Safety tip
        "Learn basic phrases in local language"       # Communication tip
    ]
