# Planventure API 🚁

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/github-samples/planventure)

A Flask-based REST API backend for trip planning and management with JWT authentication.

## ✅ Completed Features

### 🔐 Authentication System

- **User Registration** with email validation and password strength requirements
- **User Login** with JWT token generation
- **Password Security** using bcrypt hashing with salt
- **JWT Token Management** with access and refresh tokens
- **Email Format Validation** using regex patterns

### 🛡️ Security & Middleware

- **Authentication Middleware** with required/optional protection
- **Protected Routes** using decorators
- **User Authorization** - users can only access their own data
- **Error Handling** with comprehensive error responses
- **CORS Configuration** for frontend integration

### 🗺️ Trip Management (CRUD)

- **Create Trips** with validation (destination, dates, coordinates, itinerary)
- **Read Trips** with pagination and filtering
- **Update Trips** with partial updates and validation
- **Delete Trips** with proper authorization
- **Search Trips** by destination, date range, and other criteria
- **Itinerary Management** with JSON storage for trip details

### 🔧 Development Tools

- **Database Models** with SQLAlchemy relationships
- **Database Initialization** scripts
- **API Testing** with complete Bruno collection
- **Environment Configuration** with secure secret generation
- **Route Debugging** with endpoint listing

## 🚀 API Endpoints

### Authentication Routes

```
POST   /auth/register           - User registration
POST   /auth/login              - User login with JWT tokens
POST   /auth/validate-email     - Email format validation
```

### Trip Management Routes

```
POST   /trips                   - Create new trip
GET    /trips                   - Get user's trips (with pagination)
GET    /trips/<id>              - Get specific trip by ID
PUT    /trips/<id>              - Update specific trip
DELETE /trips/<id>              - Delete specific trip
GET    /trips/search            - Search trips by criteria
```

### Testing & Utility Routes

```
GET    /                        - Welcome message
GET    /health                  - Health check
GET    /routes                  - List all available routes
GET    /api/profile             - User profile (protected)
GET    /api/test-auth           - Test authentication
GET    /api/test-auth-optional  - Test optional authentication
GET    /api/public-data         - Public data with auth enhancements
```

## 🛠️ Technology Stack

- **Backend Framework**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite (development)
- **Authentication**: Flask-JWT-Extended with bcrypt
- **Security**: JWT tokens, password hashing, CORS
- **Testing**: Bruno API Client with automated token management
- **Environment**: Python virtual environment with dotenv

## 📚 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Bruno API Client (for testing)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/kdornadula/planventure.git
   cd planventure/planventure-api
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Generate secure keys**

   ```bash
   python generate_secrets.py
   ```

5. **Initialize database**

   ```bash
   python create_db.py
   ```

6. **Start the server**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

### Testing with Bruno

1. **Import the Bruno collection** from the `bruno-api-tests` folder
2. **Set up environment variables**:
   - `base_url`: `http://localhost:5000`
   - `access_token`: (auto-populated after login)
3. **Test the authentication flow**:
   - Register a new user
   - Login to get JWT tokens
   - Test protected routes

## 📝 API Usage Examples

### Create a Trip

```bash
POST /trips
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "destination": "Paris, France",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "itinerary": {
    "day1": "Visit Eiffel Tower",
    "day2": "Louvre Museum",
    "day3": "Notre-Dame Cathedral"
  }
}
```

### Get User's Trips with Pagination

```bash
GET /trips?page=1&per_page=5&destination=Paris
Authorization: Bearer <jwt_token>
```

### Search Trips

```bash
GET /trips/search?destination=Paris&start_date=2024-06-01&end_date=2024-12-31
Authorization: Bearer <jwt_token>
```

## 🔧 Project Structure

```
planventure/
├── planventure-api/              # Flask API backend
│   ├── models/                   # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model with authentication
│   │   └── trip.py              # Trip model with relationships
│   ├── routes/                   # API route blueprints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── trips.py             # Trip CRUD routes
│   │   └── protected_example.py # Example protected routes
│   ├── utils/                    # Utilities and middleware
│   │   ├── __init__.py
│   │   ├── auth.py              # JWT token utilities
│   │   └── middleware.py        # Authentication middleware
│   ├── bruno-api-tests/          # Bruno API testing collection
│   ├── app.py                    # Main Flask application
│   ├── requirements.txt          # Python dependencies
│   ├── .sample.env              # Environment variables template
│   ├── create_db.py             # Database initialization
│   └── generate_secrets.py      # Secret key generation
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔒 Security Features

- **JWT Authentication** with access and refresh tokens
- **Password Hashing** using bcrypt with automatic salt generation
- **Email Validation** with regex pattern matching
- **Route Protection** with authentication middleware
- **User Authorization** ensuring users can only access their own data
- **CORS Protection** with configurable origins
- **Environment Variables** for sensitive configuration
- **Input Validation** with comprehensive error handling

## 🧪 Testing

The project includes a comprehensive Bruno API testing collection with:

- **Authentication flow testing** (register, login, token management)
- **CRUD operations testing** for trips
- **Error handling verification**
- **Authorization testing** (protected routes)
- **Automated JWT token management**

## 🎯 Future Enhancements

- [ ] Trip sharing and collaboration features
- [ ] Advanced itinerary planning with activities
- [ ] Photo and document attachments
- [ ] Trip recommendations and suggestions
- [ ] Real-time collaboration features
- [ ] Mobile app integration
- [ ] Social features (trip reviews, ratings)
- [ ] Integration with travel APIs (flights, hotels)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask and SQLAlchemy communities
- JWT.io for token format specifications
- Bruno API Client for excellent testing tools
- GitHub Copilot for development assistance
