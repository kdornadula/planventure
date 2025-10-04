import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline, Box, Button } from "@mui/material";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/layout/Navbar";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import CreateTripPage from "./pages/CreateTripPage";
import RegisterPage from "./pages/RegisterPage";
import TripDetailsPage from "./pages/TripDetailsPage";
import EditTripPage from "./pages/EditTripPage";
import TripsPage from "./pages/TripsPage";
import ProtectedRoute from "./components/ProtectedRoute";

// Create Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
  typography: {
    fontFamily: "Roboto, Arial, sans-serif",
  },
});

// Enhanced HomePage component
const HomePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();

  return (
    <Box sx={{ p: 3, textAlign: "center" }}>
      <h1>Welcome to Planventure!</h1>

      {isAuthenticated() ? (
        <>
          <p>
            Welcome back, {user?.email_address?.split("@")[0]}! Ready for your
            next adventure?
          </p>
          <Box
            sx={{
              mt: 3,
              gap: 2,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Button variant="contained" onClick={() => navigate("/dashboard")}>
              Go to Dashboard
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate("/trips/create")}
            >
              Create New Trip
            </Button>
          </Box>
        </>
      ) : (
        <>
          <p>Your trip planning adventure starts here.</p>
          <Box
            sx={{
              mt: 3,
              gap: 2,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Button variant="contained" onClick={() => navigate("/login")}>
              Login
            </Button>
            <Button variant="outlined" onClick={() => navigate("/register")}>
              Create Account
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Box sx={{ flexGrow: 1 }}>
            <Navbar />
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Protected Routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/trips"
                element={
                  <ProtectedRoute>
                    <TripsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/trips/create"
                element={
                  <ProtectedRoute>
                    <CreateTripPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/trips/:tripId"
                element={
                  <ProtectedRoute>
                    <TripDetailsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/trips/:tripId/edit"
                element={
                  <ProtectedRoute>
                    <EditTripPage />
                  </ProtectedRoute>
                }
              />

              {/* Redirect unknown routes to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Box>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
