import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
} from "@mui/material";
import { Flight, ExitToApp } from "@mui/icons-material";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleLogin = () => {
    navigate("/login");
  };

  const handleHome = () => {
    navigate(isAuthenticated() ? "/dashboard" : "/");
  };

  return (
    <AppBar position="static" sx={{ backgroundColor: "#1976d2" }}>
      <Toolbar>
        {/* Logo and App Name */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="home"
          onClick={handleHome}
          sx={{ mr: 2 }}
        >
          <Flight />
        </IconButton>

        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: "pointer" }}
          onClick={handleHome}
        >
          Planventure
        </Typography>

        {/* Navigation Items */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {isAuthenticated() ? (
            <>
              {/* Authenticated User Menu */}
              <Typography variant="body2">
                Welcome, {user?.email_address}
              </Typography>

              <Button color="inherit" onClick={() => navigate("/dashboard")}>
                Dashboard
              </Button>

              <Button color="inherit" onClick={() => navigate("/trips")}>
                My Trips
              </Button>

              {/* Home Button for authenticated users */}
              <Button color="inherit" onClick={() => navigate("/")}>
                Home
              </Button>

              <Button
                color="inherit"
                startIcon={<ExitToApp />}
                onClick={handleLogout}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              {/* Guest Menu */}
              <Button color="inherit" onClick={() => navigate("/")}>
                Home
              </Button>

              <Button color="inherit" onClick={handleLogin}>
                Login
              </Button>

              <Button
                color="inherit"
                variant="outlined"
                onClick={() => navigate("/register")}
                sx={{
                  ml: 1,
                  borderColor: "white",
                  "&:hover": {
                    borderColor: "white",
                    backgroundColor: "rgba(255, 255, 255, 0.1)",
                  },
                }}
              >
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
