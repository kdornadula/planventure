# Planventure - Complete Full-Stack Trip Planning Application 🚁

A modern, full-featured trip planning solution with Flask REST API backend and React frontend.

## 🏗️ Project Structure

```
planventure/
├── planventure-api/              # Flask REST API Backend
│   ├── models/                   # Database models
│   ├── routes/                   # API endpoints
│   ├── utils/                    # Utilities and middleware
│   ├── bruno-api-tests/          # API testing collection
│   └── app.py                    # Main Flask application
├── planventure-frontend/         # React Frontend Application
│   ├── src/
│   │   ├── components/           # Reusable React components
│   │   ├── pages/               # Page components
│   │   ├── context/             # React context providers
│   │   └── services/            # API client services
│   ├── public/                  # Static assets
│   └── package.json             # Frontend dependencies
├── docs/                        # Project documentation
└── README.md                    # This file
```

## 🚀 Quick Start

### Backend (Flask API)

```bash
cd planventure-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python generate_secrets.py
python create_db.py
python app.py
```

### Frontend (React Application)

```bash
cd planventure-frontend
npm install
npm start
```

## ✅ Complete Feature Set

### 🔐 Authentication System

- **User Registration** with comprehensive validation and auto-login
- **User Login** with JWT token management and protected routes
- **Route Protection** with automatic redirects and return navigation
- **Password Security** using bcrypt hashing with salt
- **Email Format Validation** with real-time feedback
- **Session Management** with persistent login state

### 🛡️ Security & Middleware

- **JWT Authentication** with access and refresh tokens
- **Protected Route Components** with loading states
- **User Authorization** ensuring data isolation
- **Comprehensive Error Handling** with user-friendly messages
- **CORS Configuration** optimized for React frontend
- **Input Validation** across all forms and API endpoints

### 🗺️ Complete Trip Management

#### **Dashboard**

- **Trip Overview** with welcome personalization
- **Quick Actions** for creating and managing trips
- **Recent Trips Display** with visual cards
- **Empty State Handling** for new users

#### **My Trips Page**

- **Complete Trip Listing** with search and pagination
- **Advanced Search** by destination with real-time filtering
- **Pagination Support** for handling large trip collections
- **Trip Cards** with comprehensive information display

#### **Trip Creation**

- **Intuitive Form Interface** with date pickers and validation
- **Smart Template Generation** using Flask API endpoints
- **Multiple Trip Types** (leisure, business, adventure, cultural)
- **Coordinate Integration** with optional location data
- **Custom Itinerary Support** with JSON and text formats

#### **Trip Details View**

- **Comprehensive Trip Display** with formatted information
- **Interactive Itinerary** with day-by-day breakdown
- **Google Maps Integration** for location visualization
- **Trip Metadata** showing creation and update timestamps
- **Action Buttons** for editing and deletion

#### **Trip Editing**

- **Pre-populated Forms** with existing trip data
- **Template Regeneration** for itinerary updates
- **Partial Update Support** for efficient data management
- **Change Detection** to prevent unnecessary API calls

#### **Trip Deletion**

- **Professional Confirmation Dialogs** with trip details
- **Loading States** during deletion process
- **Immediate UI Updates** after successful deletion
- **Error Recovery** with user feedback

### 🎨 User Interface & Experience

- **Material-UI Design System** with consistent theming
- **Responsive Design** optimized for mobile and desktop
- **Professional Navigation** with breadcrumbs and clear paths
- **Loading States** and progress indicators throughout
- **Error Boundaries** with graceful error handling
- **Accessibility Features** with proper ARIA labels
- **Interactive Feedback** with hover states and animations

### 🔧 Technical Features

#### **Frontend Architecture**

- **Modern React 19** with hooks and functional components
- **React Router v6** for client-side navigation
- **Context API** for state management
- **Axios Integration** for API communication
- **Material-UI v7** for component library
- **Responsive Grid System** for layout management

#### **Backend Integration**

- **RESTful API Design** with proper HTTP methods
- **Real-time Data Sync** between frontend and backend
- **Smart Template Generation** with city-specific suggestions
- **Comprehensive Error Handling** across the stack
- **Health Monitoring** with multiple diagnostic endpoints

#### **Development Tools**

- **Hot Reload** for rapid development
- **Environment Configuration** for different deployment stages
- **API Testing** with complete Bruno collection
- **Code Organization** with modular component structure
- **Error Logging** with detailed debugging information

## 🚀 Application Pages

### **Public Pages**

- **Home Page** with conditional content based on authentication
- **Login Page** with email/password authentication
- **Registration Page** with comprehensive validation

### **Protected Pages**

- **Dashboard** - Trip overview and quick actions
- **My Trips** - Complete trip listing with search and pagination
- **Create Trip** - Trip creation with template generation
- **Trip Details** - Comprehensive trip information display
- **Edit Trip** - Trip modification with pre-populated data

### **Navigation Features**

- **Dynamic Navbar** with authentication-aware menu items
- **Breadcrumb Navigation** for clear page hierarchy
- **Mobile-Friendly** navigation with responsive design
- **Quick Actions** accessible from multiple pages

## 🛠️ Technology Stack

### **Frontend**

- **React 19** - Modern JavaScript framework
- **Material-UI v7** - Professional component library
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API communication
- **React Context** - State management
- **Material Icons** - Professional icon system

### **Backend**

- **Flask 2.3.3** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-JWT-Extended** - JWT authentication
- **bcrypt** - Password hashing
- **SQLite** - Development database

### **Development Tools**

- **Bruno API Client** - API testing and documentation
- **Node.js** - JavaScript runtime for frontend
- **Python Virtual Environment** - Backend isolation
- **Git** - Version control

## 📚 Getting Started

### Prerequisites

- **Python 3.8+** for backend development
- **Node.js 16+** and npm for frontend development
- **Git** for version control
- **Bruno API Client** for API testing (optional)

### Complete Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/kdornadula/planventure.git
   cd planventure
   ```

2. **Backend Setup**

   ```bash
   cd planventure-api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python generate_secrets.py
   python create_db.py
   ```

3. **Frontend Setup**

   ```bash
   cd ../planventure-frontend
   npm install
   ```

4. **Start Development Servers**

   **Terminal 1 - Backend:**

   ```bash
   cd planventure-api
   source venv/bin/activate
   python app.py
   # Runs on http://localhost:5000
   ```

   **Terminal 2 - Frontend:**

   ```bash
   cd planventure-frontend
   npm start
   # Runs on http://localhost:3000
   ```

5. **Access the Application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:5000`
   - API Health Check: `http://localhost:5000/health`

## 📝 API Usage Examples

### Authentication Flow

```bash
# Register new user
POST http://localhost:5000/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

# Login user
POST http://localhost:5000/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Trip Management

```bash
# Create trip
POST http://localhost:5000/trips
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "destination": "Tokyo, Japan",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "itinerary": {
    "day1": "Arrive and explore Shibuya",
    "day2": "Visit Senso-ji Temple",
    "day3": "Day trip to Mount Fuji"
  }
}

# Get user's trips with pagination
GET http://localhost:5000/trips?page=1&per_page=5
Authorization: Bearer <jwt_token>

# Generate itinerary template
GET http://localhost:5000/trips/template?destination=Paris&start_date=2024-06-01&end_date=2024-06-05&trip_type=leisure
Authorization: Bearer <jwt_token>
```

## 🔒 Security Features

- **JWT Authentication** with secure token management
- **Password Hashing** using bcrypt with automatic salt generation
- **Protected Routes** with automatic authentication checks
- **User Data Isolation** ensuring users only access their own data
- **CORS Protection** with configurable origins
- **Input Validation** preventing malicious data injection
- **Environment Variables** for secure configuration management
- **Session Management** with automatic token refresh handling

## 🧪 Testing

### Backend Testing

- **Bruno API Collection** with comprehensive endpoint testing
- **Authentication Flow Testing** for registration and login
- **CRUD Operation Testing** for all trip management features
- **Template Generation Testing** for itinerary creation
- **Error Handling Verification** for edge cases

### Frontend Testing

- **Component Integration Testing** for user flows
- **Authentication Testing** for login/logout functionality
- **Form Validation Testing** for all input forms
- **Navigation Testing** for route protection and redirects
- **API Integration Testing** for frontend-backend communication

## 🎯 Complete User Journey

1. **Registration/Login** - User creates account or logs in
2. **Dashboard Welcome** - Personalized greeting and trip overview
3. **Trip Creation** - User creates trip with template assistance
4. **Trip Management** - User views, searches, and organizes trips
5. **Trip Details** - User views comprehensive trip information
6. **Trip Editing** - User modifies trip details and itinerary
7. **Trip Deletion** - User removes trips with confirmation

## 🌟 Key Achievements

### **Full-Stack Integration**

- ✅ Complete React frontend with Flask backend integration
- ✅ Real-time data synchronization across the application
- ✅ Professional API design with RESTful endpoints
- ✅ Seamless authentication flow with JWT tokens

### **User Experience Excellence**

- ✅ Intuitive interface with Material-UI design system
- ✅ Responsive design working on all device sizes
- ✅ Smart template generation for trip planning assistance
- ✅ Comprehensive error handling with user-friendly messages

### **Production Readiness**

- ✅ Security best practices with protected routes and data validation
- ✅ Scalable architecture with modular component design
- ✅ Comprehensive testing coverage with Bruno API tests
- ✅ Professional development practices with proper documentation

## 🚀 Future Enhancement Ideas

- [ ] **Trip Sharing** - Collaborate on trips with other users
- [ ] **Photo Management** - Upload and organize trip photos
- [ ] **Expense Tracking** - Budget management and expense logging
- [ ] **Weather Integration** - Real-time weather data for destinations
- [ ] **Map Visualization** - Interactive maps for trip planning
- [ ] **Mobile App** - React Native version for mobile devices
- [ ] **Offline Support** - PWA features for offline trip access
- [ ] **Social Features** - Trip reviews, ratings, and recommendations
- [ ] **Calendar Integration** - Sync with external calendar apps
- [ ] **Export Features** - PDF trip itineraries and backup options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask and SQLAlchemy** communities for excellent backend frameworks
- **React and Material-UI** teams for modern frontend development tools
- **JWT.io** for token format specifications and security guidance
- **Bruno API Client** for professional API testing capabilities
- **GitHub Copilot** for development assistance and code suggestions
- **Open Source Community** for inspiration and best practices

---

**Built with ❤️ using modern web technologies for the ultimate trip planning experience!** ✈️🗺️
