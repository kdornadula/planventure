import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
} from "@mui/material";
import { Flight, ExitToApp, Menu as MenuIcon } from "@mui/icons-material";
import { useAuth } from "../../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuAnchor, setMobileMenuAnchor] = React.useState(null);

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

  const handleMobileMenuOpen = (event) => {
    setMobileMenuAnchor(event.currentTarget);
  };

  const handleMobileMenuClose = () => {
    setMobileMenuAnchor(null);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            fontSize: { xs: "1rem", sm: "1.25rem" }, // Smaller font on mobile
          }}
        >
          <Flight sx={{ mr: 1, verticalAlign: "middle" }} />
          Planventure
        </Typography>

        {/* Mobile Menu */}
        <Box sx={{ display: { xs: "flex", md: "none" } }}>
          <IconButton
            size="large"
            onClick={handleMobileMenuOpen}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
        </Box>

        {/* Desktop Menu */}
        <Box sx={{ display: { xs: "none", md: "flex" } }}>
          {isAuthenticated() ? (
            <>
              {/* Authenticated User Menu */}
              <Typography variant="body2">
                Welcome, {user?.email_address}
              </Typography>

              <Button
                color="inherit"
                component={Link}
                to="/dashboard"
                sx={{ mx: 1, minWidth: "auto" }}
              >
                Dashboard
              </Button>

              <Button
                color="inherit"
                onClick={() => navigate("/trips")}
                sx={{ mx: 1, minWidth: "auto" }}
              >
                My Trips
              </Button>

              {/* Home Button for authenticated users */}
              <Button
                color="inherit"
                onClick={() => navigate("/")}
                sx={{ mx: 1, minWidth: "auto" }}
              >
                Home
              </Button>

              <Button
                color="inherit"
                startIcon={<ExitToApp />}
                onClick={handleLogout}
                sx={{ mx: 1, minWidth: "auto" }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              {/* Guest Menu */}
              <Button
                color="inherit"
                onClick={() => navigate("/")}
                sx={{ mx: 1, minWidth: "auto" }}
              >
                Home
              </Button>

              <Button
                color="inherit"
                onClick={handleLogin}
                sx={{ mx: 1, minWidth: "auto" }}
              >
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

        {/* Mobile Menu Drawer */}
        <Menu
          anchorEl={mobileMenuAnchor}
          open={Boolean(mobileMenuAnchor)}
          onClose={handleMobileMenuClose}
          sx={{ display: { xs: "block", md: "none" } }}
        >
          {/* Mobile menu items */}
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
