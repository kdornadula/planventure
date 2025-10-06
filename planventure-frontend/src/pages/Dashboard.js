import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  CircularProgress,
} from "@mui/material";
import { Add, Flight } from "@mui/icons-material";
import { useAuth } from "../context/AuthContext";
import { tripsAPI } from "../services/api";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      const response = await tripsAPI.getTrips({ page: 1, per_page: 10 });
      setTrips(response.data.trips || []);
    } catch (err) {
      setError("Failed to load trips");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" style={{ marginTop: 20, padding: 20 }}>
      <Box style={{ textAlign: "center", marginBottom: 30 }}>
        <Flight style={{ fontSize: 40, color: "#1976d2", marginBottom: 10 }} />
        <Typography variant="h4" gutterBottom>
          Welcome back, {user?.email_address?.split("@")[0]}!
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Ready to plan your next adventure?
        </Typography>
      </Box>

      {error && (
        <Typography color="error" style={{ marginBottom: 20 }}>
          {error}
        </Typography>
      )}

      <Box style={{ textAlign: "center", marginBottom: 30 }}>
        <Typography variant="h5" gutterBottom>
          Your Trips
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => navigate("/trips/create")}
          style={{ marginBottom: 20 }}
        >
          Create New Trip
        </Button>
      </Box>

      {loading ? (
        <Box style={{ textAlign: "center", padding: 40 }}>
          <CircularProgress />
        </Box>
      ) : trips.length === 0 ? (
        <Box style={{ textAlign: "center", padding: 40 }}>
          <Typography variant="h6" gutterBottom>
            No trips yet
          </Typography>
          <Typography variant="body2" style={{ marginBottom: 20 }}>
            Start planning your first adventure!
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate("/trips/create")}
          >
            Create Your First Trip
          </Button>
        </Box>
      ) : (
        <Box>
          {trips.map((trip) => (
            <Box
              key={trip.id}
              style={{
                border: "1px solid #ddd",
                padding: 20,
                marginBottom: 20,
                borderRadius: 8,
              }}
            >
              <Typography variant="h6">{trip.destination}</Typography>
              <Typography variant="body2">
                {trip.start_date} - {trip.end_date}
              </Typography>
              <Button
                onClick={() => navigate(`/trips/${trip.id}`)}
                style={{ marginTop: 10 }}
              >
                View Details
              </Button>
            </Box>
          ))}
        </Box>
      )}
    </Container>
  );
};

export default Dashboard;
