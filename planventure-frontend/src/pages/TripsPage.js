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
  Paper,
  TextField,
  InputAdornment,
  Pagination,
  Breadcrumbs,
  Link,
} from "@mui/material";
import {
  Add,
  Flight,
  CalendarToday,
  LocationOn,
  Edit,
  Delete,
  Search,
  Home,
} from "@mui/icons-material";
import { useAuth } from "../context/AuthContext";
import { tripsAPI } from "../services/api";
import { useNavigate } from "react-router-dom";
import ConfirmDialog from "../components/ConfirmDialog";

const TripsPage = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [deleteDialog, setDeleteDialog] = useState({
    open: false,
    tripId: null,
    tripDestination: "",
    loading: false,
  });
  const { user } = useAuth();
  const navigate = useNavigate();

  // Fetch trips when component loads or search/page changes
  useEffect(() => {
    fetchTrips();
  }, [currentPage, searchTerm]);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await tripsAPI.getTrips({
        page: currentPage,
        per_page: 6,
        destination: searchTerm || undefined,
      });

      setTrips(response.data.trips || []);
      setTotalPages(response.data.pagination?.pages || 1);
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

  // Handle search
  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1); // Reset to first page when searching
  };

  // Handle page change
  const handlePageChange = (event, page) => {
    setCurrentPage(page);
  };

  // Handle trip deletion
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
      setError("");

      await tripsAPI.deleteTrip(deleteDialog.tripId);

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
      setDeleteDialog((prev) => ({ ...prev, loading: false, open: false }));
    }
  };

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
        <Typography color="text.primary">My Trips</Typography>
      </Breadcrumbs>

      {/* Header */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box
          display="flex"
          alignItems="center"
          justifyContent="space-between"
          mb={3}
        >
          <Box display="flex" alignItems="center">
            <Flight sx={{ fontSize: 40, color: "primary.main", mr: 2 }} />
            <Box>
              <Typography variant="h4" component="h1" gutterBottom>
                My Trips
              </Typography>
              <Typography variant="subtitle1" color="textSecondary">
                All your adventures, {user?.email_address?.split("@")[0]}
              </Typography>
            </Box>
          </Box>

          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate("/trips/create")}
          >
            Create New Trip
          </Button>
        </Box>

        {/* Search */}
        <TextField
          fullWidth
          placeholder="Search trips by destination..."
          value={searchTerm}
          onChange={handleSearch}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
          sx={{ maxWidth: 400 }}
        />
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Loading State */}
      {loading ? (
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      ) : trips.length === 0 ? (
        /* Empty State */
        <Paper sx={{ p: 6, textAlign: "center", bgcolor: "grey.50" }}>
          <Flight sx={{ fontSize: 60, color: "grey.400", mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            {searchTerm ? "No trips found" : "No trips yet"}
          </Typography>
          <Typography variant="body2" color="textSecondary" mb={3}>
            {searchTerm
              ? `No trips match "${searchTerm}". Try a different search term.`
              : "Start planning your first adventure!"}
          </Typography>
          {!searchTerm && (
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate("/trips/create")}
            >
              Create Your First Trip
            </Button>
          )}
        </Paper>
      ) : (
        <>
          {/* Results Summary */}
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            {searchTerm
              ? `Found ${trips.length} trip${
                  trips.length !== 1 ? "s" : ""
                } matching "${searchTerm}"`
              : `Showing ${trips.length} trip${trips.length !== 1 ? "s" : ""}`}
          </Typography>

          {/* Trips Grid */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            {trips.map((trip) => (
              <Grid item xs={12} sm={6} md={4} key={trip.id}>
                <Card
                  sx={{
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    "&:hover": { boxShadow: 4 },
                  }}
                >
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" component="h3" gutterBottom>
                      {trip.destination}
                    </Typography>

                    <Box display="flex" alignItems="center" mb={1}>
                      <CalendarToday
                        sx={{ fontSize: 16, mr: 1, color: "grey.600" }}
                      />
                      <Typography variant="body2" color="textSecondary">
                        {formatDate(trip.start_date)} -{" "}
                        {formatDate(trip.end_date)}
                      </Typography>
                    </Box>

                    <Chip
                      label={`${getTripDuration(
                        trip.start_date,
                        trip.end_date
                      )} days`}
                      size="small"
                      sx={{ mb: 2 }}
                    />

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

                  <CardActions sx={{ justifyContent: "space-between" }}>
                    <Button
                      size="small"
                      onClick={() => navigate(`/trips/${trip.id}`)}
                    >
                      View Details
                    </Button>
                    <Box>
                      <Button
                        size="small"
                        startIcon={<Edit />}
                        onClick={() => navigate(`/trips/${trip.id}/edit`)}
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
                        sx={{ ml: 1 }}
                      >
                        Delete
                      </Button>
                    </Box>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Pagination */}
          {totalPages > 1 && (
            <Box display="flex" justifyContent="center">
              <Pagination
                count={totalPages}
                page={currentPage}
                onChange={handlePageChange}
                color="primary"
                size="large"
              />
            </Box>
          )}
        </>
      )}

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

export default TripsPage;
