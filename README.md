# Planventure API 🚁

A Flask-based REST API backend for trip planning and management.

## ✅ Completed Features

- **User Authentication**: Registration, login with JWT tokens
- **Password Security**: bcrypt hashing with salt
- **Protected Routes**: Middleware for required/optional authentication
- **Database Models**: User and Trip models with relationships
- **API Testing**: Complete Bruno collection for testing
- **Email Validation**: Regex-based email format validation
- **Error Handling**: Comprehensive error responses

## 🚀 API Endpoints

### Authentication

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/validate-email` - Email validation

### Protected Routes

- `GET /api/profile` - Get user profile (auth required)
- `PUT /api/profile` - Update profile (auth required)
- `GET /api/public-data` - Public data with optional auth enhancements
- `GET /api/test-auth` - Test authentication (auth required)
- `GET /api/test-auth-optional` - Test optional authentication

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended
- **Database**: SQLite (development)
- **Security**: bcrypt, JWT tokens
- **Testing**: Bruno API Client
- **Environment**: Python virtual environment

## 📚 Getting Started

See the [planventure-api README](./planventure-api/README.md) for detailed setup instructions.

## 🔗 Project Structure

```
planventure/
├── planventure-api/          # Flask API backend
│   ├── models/              # Database models
│   ├── routes/              # API route blueprints
│   ├── utils/               # Utilities and middleware
│   ├── app.py               # Main Flask application
│   └── requirements.txt     # Python dependencies
└── README.md               # This file
```

## 🎯 Next Steps

- [ ] Trip CRUD operations
- [ ] Trip sharing functionality
- [ ] Itinerary management
- [ ] React frontend integration
- GET / - Welcome message
- GET /health - Health check endpoint

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
