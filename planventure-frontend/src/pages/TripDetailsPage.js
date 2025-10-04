import React, { useState, useEffect } from "react";
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  Card,
  CardContent,
  IconButton,
  Breadcrumbs,
  Link,
} from "@mui/material";
import {
  ArrowBack,
  Edit,
  Delete,
  Flight,
  CalendarToday,
  LocationOn,
  Schedule,
  Map,
  Home,
} from "@mui/icons-material";
import { useParams, useNavigate } from "react-router-dom";
import { tripsAPI } from "../services/api";
import { useAuth } from "../context/AuthContext";

const TripDetailsPage = () => {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  // State
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Fetch trip details when component loads
  useEffect(() => {
    fetchTripDetails();
  }, [tripId]);

  const fetchTripDetails = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await tripsAPI.getTrip(tripId);
      setTrip(response.data.trip);
    } catch (err) {
      console.error("Error fetching trip details:", err);
      if (err.response?.status === 404) {
        setError("Trip not found or you do not have permission to view it.");
      } else {
        setError("Failed to load trip details. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      weekday: "long",
    });
  };

  // Calculate trip duration
  const getTripDuration = (startDate, endDate) => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  // Handle trip deletion
  const handleDeleteTrip = async () => {
    if (
      window.confirm(
        "Are you sure you want to delete this trip? This action cannot be undone."
      )
    ) {
      try {
        setDeleteLoading(true);
        await tripsAPI.deleteTrip(tripId);
        navigate("/dashboard");
      } catch (err) {
        console.error("Error deleting trip:", err);
        setError("Failed to delete trip. Please try again.");
      } finally {
        setDeleteLoading(false);
      }
    }
  };

  // Parse itinerary data
  const parseItinerary = (itineraryData) => {
    if (!itineraryData) return null;

    try {
      if (typeof itineraryData === "string") {
        return JSON.parse(itineraryData);
      }
      return itineraryData;
    } catch {
      return { notes: itineraryData };
    }
  };

  // Loading state
  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  // Error state
  if (error && !trip) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate("/dashboard")}
        >
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  const itinerary = parseItinerary(trip?.itinerary);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link
          color="inherit"
          href="#"
          onClick={() => navigate("/")}
          sx={{ display: "flex", alignItems: "center" }}
        >
          <Home sx={{ mr: 0.5 }} fontSize="inherit" />
          Home
        </Link>
        <Link color="inherit" href="#" onClick={() => navigate("/dashboard")}>
          Dashboard
        </Link>
        <Typography color="text.primary">Trip Details</Typography>
      </Breadcrumbs>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Trip Header */}
      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={8}>
            <Box display="flex" alignItems="center" mb={2}>
              <Flight sx={{ fontSize: 40, color: "primary.main", mr: 2 }} />
              <Box>
                <Typography variant="h4" component="h1" gutterBottom>
                  {trip?.destination}
                </Typography>
                <Typography variant="subtitle1" color="textSecondary">
                  Trip #{trip?.id} • Created by{" "}
                  {user?.email_address?.split("@")[0]}
                </Typography>
              </Box>
            </Box>

            {/* Trip Info Cards */}
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item xs={12} sm={6} md={4}>
                <Card variant="outlined" sx={{ textAlign: "center", p: 2 }}>
                  <CalendarToday
                    sx={{ fontSize: 30, color: "primary.main", mb: 1 }}
                  />
                  <Typography variant="h6">Start Date</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {formatDate(trip?.start_date)}
                  </Typography>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6} md={4}>
                <Card variant="outlined" sx={{ textAlign: "center", p: 2 }}>
                  <CalendarToday
                    sx={{ fontSize: 30, color: "secondary.main", mb: 1 }}
                  />
                  <Typography variant="h6">End Date</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {formatDate(trip?.end_date)}
                  </Typography>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6} md={4}>
                <Card variant="outlined" sx={{ textAlign: "center", p: 2 }}>
                  <Schedule
                    sx={{ fontSize: 30, color: "success.main", mb: 1 }}
                  />
                  <Typography variant="h6">Duration</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {getTripDuration(trip?.start_date, trip?.end_date)} days
                  </Typography>
                </Card>
              </Grid>
            </Grid>
          </Grid>

          {/* Action Buttons */}
          <Grid item xs={12} md={4}>
            <Box display="flex" flexDirection="column" gap={2}>
              <Button
                variant="contained"
                startIcon={<Edit />}
                onClick={() => navigate(`/trips/${tripId}/edit`)}
                fullWidth
              >
                Edit Trip
              </Button>

              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={handleDeleteTrip}
                disabled={deleteLoading}
                fullWidth
              >
                {deleteLoading ? <CircularProgress size={20} /> : "Delete Trip"}
              </Button>

              <Button
                variant="outlined"
                startIcon={<ArrowBack />}
                onClick={() => navigate("/dashboard")}
                fullWidth
              >
                Back to Dashboard
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Location Info */}
      {trip?.coordinates && (
        <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
          <Typography
            variant="h6"
            gutterBottom
            sx={{ display: "flex", alignItems: "center" }}
          >
            <LocationOn sx={{ mr: 1 }} />
            Location
          </Typography>
          <Typography variant="body1">
            Coordinates: {trip.coordinates.latitude?.toFixed(4)},{" "}
            {trip.coordinates.longitude?.toFixed(4)}
          </Typography>
          <Button
            variant="outlined"
            startIcon={<Map />}
            sx={{ mt: 2 }}
            onClick={() =>
              window.open(
                `https://www.google.com/maps?q=${trip.coordinates.latitude},${trip.coordinates.longitude}`,
                "_blank"
              )
            }
          >
            View on Google Maps
          </Button>
        </Paper>
      )}

      {/* Itinerary Section */}
      {itinerary && (
        <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Itinerary
          </Typography>
          <Divider sx={{ mb: 3 }} />

          {typeof itinerary === "object" && itinerary !== null ? (
            Object.entries(itinerary).map(([day, activities], index) => (
              <Card key={index} variant="outlined" sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    {day}
                  </Typography>

                  {typeof activities === "object" && activities !== null ? (
                    Object.entries(activities).map(([timeOfDay, activity]) => (
                      <Box key={timeOfDay} sx={{ mb: 1 }}>
                        <Chip
                          label={
                            timeOfDay.charAt(0).toUpperCase() +
                            timeOfDay.slice(1)
                          }
                          size="small"
                          sx={{ mr: 1, mb: 1 }}
                        />
                        <Typography variant="body2" component="span">
                          {activity}
                        </Typography>
                      </Box>
                    ))
                  ) : (
                    <Typography variant="body2">{activities}</Typography>
                  )}
                </CardContent>
              </Card>
            ))
          ) : (
            <Typography variant="body1">{itinerary}</Typography>
          )}
        </Paper>
      )}

      {/* Trip Metadata */}
      <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Trip Information
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">
              Created
            </Typography>
            <Typography variant="body1">
              {new Date(trip?.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">
              Last Updated
            </Typography>
            <Typography variant="body1">
              {new Date(trip?.updated_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default TripDetailsPage;
