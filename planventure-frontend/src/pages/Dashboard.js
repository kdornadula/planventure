import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Fab,
  Paper,
} from "@mui/material";
import {
  Add,
  Flight,
  CalendarToday,
  LocationOn,
  Edit,
  Delete,
} from "@mui/icons-material";
import { useAuth } from "../context/AuthContext";
import { tripsAPI } from "../services/api";
import { useNavigate } from "react-router-dom";
import ConfirmDialog from "../components/ConfirmDialog";

const Dashboard = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleteDialog, setDeleteDialog] = useState({
    open: false,
    tripId: null,
    tripDestination: "",
    loading: false,
  });
  const { user } = useAuth();
  const navigate = useNavigate();

  // Fetch trips when component loads
  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError("");

      // Call your Flask API to get trips
      const response = await tripsAPI.getTrips({
        page: 1,
        per_page: 10,
      });

      setTrips(response.data.trips || []);
    } catch (err) {
      console.error("Error fetching trips:", err);
      setError("Failed to load trips. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
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

  // Handle trip deletion with custom dialog
  const handleDeleteTrip = (tripId, tripDestination) => {
    setDeleteDialog({
      open: true,
      tripId,
      tripDestination,
      loading: false,
    });
  };

  // Close delete dialog
  const handleCloseDeleteDialog = () => {
    if (!deleteDialog.loading) {
      setDeleteDialog({
        open: false,
        tripId: null,
        tripDestination: "",
        loading: false,
      });
    }
  };

  // Confirm trip deletion
  const handleConfirmDelete = async () => {
    try {
      setDeleteDialog((prev) => ({ ...prev, loading: true }));
      setError(""); // Clear any existing errors

      await tripsAPI.deleteTrip(deleteDialog.tripId);

      // Close dialog and refresh trips
      setDeleteDialog({
        open: false,
        tripId: null,
        tripDestination: "",
        loading: false,
      });

      // Refresh trips list
      await fetchTrips();
    } catch (err) {
      console.error("Error deleting trip:", err);
      setError(
        `Failed to delete trip to ${deleteDialog.tripDestination}. Please try again.`
      );

      // Close dialog on error
      setDeleteDialog((prev) => ({ ...prev, loading: false, open: false }));
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 2, px: { xs: 1, sm: 3 } }}>
      {/* Welcome Header */}
      <Paper sx={{ p: { xs: 2, sm: 3 }, mb: { xs: 2, sm: 4 } }}>
        <Box display="flex" alignItems="center" mb={2}>
          <Flight
            sx={{
              fontSize: { xs: 30, sm: 40 },
              color: "primary.main",
              mr: { xs: 1, sm: 2 },
            }}
          />
          <Box>
            <Typography
              variant="h4"
              component="h1"
              gutterBottom
              sx={{
                fontSize: { xs: "1.5rem", sm: "2rem", md: "2.125rem" },
              }}
            >
              Welcome back, {user?.email_address?.split("@")[0]}!
            </Typography>
            <Typography
              variant="subtitle1"
              color="textSecondary"
              sx={{ fontSize: { xs: "0.875rem", sm: "1rem" } }}
            >
              Ready to plan your next adventure?
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Trips Section */}
      <Box mb={4}>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          mb={3}
          flexDirection={{ xs: "column", sm: "row" }}
          gap={{ xs: 2, sm: 0 }}
        >
          <Typography
            variant="h5"
            component="h2"
            sx={{ fontSize: { xs: "1.25rem", sm: "1.5rem" } }}
          >
            Your Trips
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate("/trips/create")}
            fullWidth={{ xs: true, sm: false }}
            sx={{ minWidth: { sm: "auto" } }}
          >
            Create New Trip
          </Button>
        </Box>

        {/* Loading State */}
        {loading ? (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress />
          </Box>
        ) : trips.length === 0 ? (
          /* Empty State */
          <Paper
            sx={{
              p: 6,
              textAlign: "center",
              bgcolor: "grey.50",
            }}
          >
            <Flight sx={{ fontSize: 60, color: "grey.400", mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              No trips yet
            </Typography>
            <Typography variant="body2" color="textSecondary" mb={3}>
              Start planning your first adventure!
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate("/trips/create")}
            >
              Create Your First Trip
            </Button>
          </Paper>
        ) : (
          /* Trips Grid */
          <Grid container spacing={{ xs: 2, sm: 3 }}>
            {trips.map((trip) => (
              <Grid item xs={12} sm={6} lg={4} key={trip.id}>
                <Card
                  sx={{
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    "&:hover": { boxShadow: 4 },
                  }}
                >
                  <CardContent sx={{ flexGrow: 1, p: { xs: 2, sm: 3 } }}>
                    {/* Trip Destination */}
                    <Typography variant="h6" component="h3" gutterBottom>
                      {trip.destination}
                    </Typography>

                    {/* Trip Dates */}
                    <Box display="flex" alignItems="center" mb={1}>
                      <CalendarToday
                        sx={{ fontSize: 16, mr: 1, color: "grey.600" }}
                      />
                      <Typography variant="body2" color="textSecondary">
                        {formatDate(trip.start_date)} -{" "}
                        {formatDate(trip.end_date)}
                      </Typography>
                    </Box>

                    {/* Trip Duration */}
                    <Chip
                      label={`${getTripDuration(
                        trip.start_date,
                        trip.end_date
                      )} days`}
                      size="small"
                      sx={{ mb: 2 }}
                    />

                    {/* Coordinates if available */}
                    {trip.coordinates && (
                      <Box display="flex" alignItems="center">
                        <LocationOn
                          sx={{ fontSize: 16, mr: 1, color: "grey.600" }}
                        />
                        <Typography variant="body2" color="textSecondary">
                          {trip.coordinates.latitude?.toFixed(2)},{" "}
                          {trip.coordinates.longitude?.toFixed(2)}
                        </Typography>
                      </Box>
                    )}
                  </CardContent>

                  {/* Card Actions */}
                  <CardActions
                    sx={{
                      justifyContent: "space-between",
                      flexDirection: { xs: "column", sm: "row" },
                      gap: { xs: 1, sm: 0 },
                      p: { xs: 2, sm: 1 },
                    }}
                  >
                    <Button
                      size="small"
                      onClick={() => navigate(`/trips/${trip.id}`)}
                      fullWidth={{ xs: true, sm: false }}
                    >
                      View Details
                    </Button>
                    <Box
                      sx={{
                        display: "flex",
                        gap: 1,
                        width: { xs: "100%", sm: "auto" },
                      }}
                    >
                      <Button
                        size="small"
                        startIcon={<Edit />}
                        onClick={() => navigate(`/trips/${trip.id}/edit`)}
                        sx={{ flex: { xs: 1, sm: "none" } }}
                      >
                        Edit
                      </Button>
                      <Button
                        size="small"
                        color="error"
                        startIcon={<Delete />}
                        onClick={() =>
                          handleDeleteTrip(trip.id, trip.destination)
                        }
                        sx={{ flex: { xs: 1, sm: "none" } }}
                      >
                        Delete
                      </Button>
                    </Box>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      {/* Floating Action Button for Mobile */}
      <Fab
        color="primary"
        aria-label="add trip"
        sx={{
          position: "fixed",
          bottom: { xs: 16, sm: 24 },
          right: { xs: 16, sm: 24 },
          display: { xs: "flex", sm: "none" },
        }}
        onClick={() => navigate("/trips/create")}
      >
        <Add />
      </Fab>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        open={deleteDialog.open}
        onClose={handleCloseDeleteDialog}
        onConfirm={handleConfirmDelete}
        loading={deleteDialog.loading}
        title="Delete Trip"
        message={`Are you sure you want to delete your trip to "${deleteDialog.tripDestination}"? This action cannot be undone.`}
      />
    </Container>
  );
};

export default Dashboard;
