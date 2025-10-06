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
    <Container maxWidth="lg" style={{ marginTop: 16, marginBottom: 16 }}>
      {/* Welcome Header */}
      <Paper style={{ padding: 16, marginBottom: 16 }}>
        <Box display="flex" alignItems="center" mb={2}>
          <Flight
            style={{
              fontSize: 32,
              color: "#1976d2",
              marginRight: 16,
            }}
          />
          <Box>
            <Typography
              variant="h5"
              component="h1"
              gutterBottom
            >
              Welcome back, {user?.email_address?.split("@")[0]}!
            </Typography>
            <Typography
              variant="subtitle1"
              color="textSecondary"
            >
              Ready to plan your next adventure?
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" style={{ marginBottom: 24 }}>
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
          style={{ flexDirection: 'column', gap: 16 }}
        >
          <Typography variant="h6" component="h2">
            Your Trips
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate("/trips/create")}
            fullWidth
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
          <Paper style={{ padding: 24, textAlign: "center" }}>
            <Flight style={{ fontSize: 48, color: "#999", marginBottom: 16 }} />
            <Typography variant="h6" gutterBottom>
              No trips yet
            </Typography>
            <Typography variant="body2" color="textSecondary" style={{ marginBottom: 24 }}>
              Start planning your first adventure!
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate("/trips/create")}
              size="large"
            >
              Create Your First Trip
            </Button>
          </Paper>
        ) : (
          /* Trips Grid */
          <Grid container spacing={2}>
            {trips.map((trip) => (
              <Grid item xs={12} sm={6} md={4} key={trip.id}>
                <Card style={{ height: "100%", display: "flex", flexDirection: "column" }}>
                  <CardContent style={{ flexGrow: 1 }}>
                    <Typography variant="h6" component="h3" gutterBottom>
                      {trip.destination}
                    </Typography>

                    <Box display="flex" alignItems="center" mb={1}>
                      <CalendarToday style={{ fontSize: 16, marginRight: 8, color: "#666" }} />
                      <Typography variant="body2" color="textSecondary">
                        {formatDate(trip.start_date)} - {formatDate(trip.end_date)}
                      </Typography>
                    </Box>

                    <Chip
                      label={`${getTripDuration(trip.start_date, trip.end_date)} days`}
                      size="small"
                      style={{ marginBottom: 16 }}
                    />

                    {trip.coordinates && (
                      <Box display="flex" alignItems="center">
                        <LocationOn style={{ fontSize: 16, marginRight: 8, color: "#666" }} />
                        <Typography variant="body2" color="textSecondary">
                          {trip.coordinates.latitude?.toFixed(2)}, {trip.coordinates.longitude?.toFixed(2)}
                        </Typography>
                      </Box>
                    )}
                  </CardContent>

                  <CardActions style={{ padding: 16 }}>
                    <Box style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
                      <Button
                        size="small"
                        onClick={() => navigate(`/trips/${trip.id}`)}
                        fullWidth
                      >
                        View Details
                      </Button>
                      <Box style={{ display: "flex", gap: 8 }}>
                        <Button
                          size="small"
                          startIcon={<Edit />}
                          onClick={() => navigate(`/trips/${trip.id}/edit`)}
                          style={{ flex: 1 }}
                        >
                          Edit
                        </Button>
                        <Button
                          size="small"
                          color="error"
                          startIcon={<Delete />}
                          onClick={() => handleDeleteTrip(trip.id, trip.destination)}
                          style={{ flex: 1 }}
                        >
                          Delete
                        </Button>
                      </Box>
                    </Box>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      {/* Floating Action Button for Mobile - Hidden for now */}
      <style>
        {`
          @media (max-width: 600px) {
            .MuiContainer-root {
              padding-left: 8px !important;
              padding-right: 8px !important;
            }
          }
        `}
      </style>

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
                    >
                      <Button
                        size="small"
                        onClick={() => navigate(`/trips/${trip.id}`)}
                        sx={{ flex: 1 }}
                      >
                        View Details
                      </Button>
                      <Box
                        sx={{
                          display: "flex",
                          gap: 1,
                          flex: 1,
                        }}
                      >
                        <Button
                          size="small"
                          startIcon={<Edit />}
                          onClick={() => navigate(`/trips/${trip.id}/edit`)}
                          sx={{ flex: 1 }}
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
                          sx={{ flex: 1 }}
                        >
                          Delete
                        </Button>
                      </Box>
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
          bottom: 16,
          right: 16,
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
