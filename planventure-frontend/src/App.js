import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline, Box, Button, Typography } from "@mui/material";
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

// Enhanced theme with better mobile breakpoints
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
    // Better mobile typography
    h4: {
      fontSize: "2.125rem",
      "@media (max-width:600px)": {
        fontSize: "1.5rem",
      },
    },
    h5: {
      fontSize: "1.5rem",
      "@media (max-width:600px)": {
        fontSize: "1.25rem",
      },
    },
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
});

// Enhanced HomePage with better mobile layout
const HomePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();

  return (
    <Box
      sx={{
        p: { xs: 2, sm: 3 },
        textAlign: "center",
        minHeight: "calc(100vh - 64px)", // Account for navbar
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <Typography
        variant="h3"
        component="h1"
        sx={{
          fontSize: { xs: "2rem", sm: "3rem" },
          mb: { xs: 2, sm: 3 },
        }}
      >
        Welcome to Planventure!
      </Typography>

      {isAuthenticated() ? (
        <>
          <Typography
            variant="body1"
            sx={{
              fontSize: { xs: "1rem", sm: "1.125rem" },
              mb: { xs: 3, sm: 4 },
              maxWidth: "600px",
              mx: "auto",
            }}
          >
            Welcome back, {user?.email_address?.split("@")[0]}! Ready for your
            next adventure?
          </Typography>
          <Box
            sx={{
              mt: 3,
              gap: 2,
              display: "flex",
              justifyContent: "center",
              flexDirection: { xs: "column", sm: "row" },
              maxWidth: "400px",
              mx: "auto",
            }}
          >
            <Button
              variant="contained"
              onClick={() => navigate("/dashboard")}
              fullWidth={{ xs: true, sm: false }}
              size={{ xs: "large", sm: "medium" }}
            >
              Go to Dashboard
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate("/trips/create")}
              fullWidth={{ xs: true, sm: false }}
              size={{ xs: "large", sm: "medium" }}
            >
              Create New Trip
            </Button>
          </Box>
        </>
      ) : (
        <>
          <Typography
            variant="body1"
            sx={{
              fontSize: { xs: "1rem", sm: "1.125rem" },
              mb: { xs: 3, sm: 4 },
              maxWidth: "600px",
              mx: "auto",
            }}
          >
            Your trip planning adventure starts here.
          </Typography>
          <Box
            sx={{
              mt: 3,
              gap: 2,
              display: "flex",
              justifyContent: "center",
              flexDirection: { xs: "column", sm: "row" },
              maxWidth: "300px",
              mx: "auto",
            }}
          >
            <Button
              variant="contained"
              onClick={() => navigate("/login")}
              fullWidth={{ xs: true, sm: false }}
              size={{ xs: "large", sm: "medium" }}
            >
              Login
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate("/register")}
              fullWidth={{ xs: true, sm: false }}
              size={{ xs: "large", sm: "medium" }}
            >
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
