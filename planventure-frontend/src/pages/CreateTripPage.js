import React, { useState } from "react";
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Grid,
  MenuItem,
  Divider,
} from "@mui/material";
import { Flight, LocationOn, Save, AutoAwesome } from "@mui/icons-material";
import { tripsAPI } from "../services/api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const CreateTripPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Form state
  const [formData, setFormData] = useState({
    destination: "",
    startDate: "",
    endDate: "",
    latitude: "",
    longitude: "",
    tripType: "leisure",
    customItinerary: "",
  });

  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [generatedTemplate, setGeneratedTemplate] = useState(null);
  const [showTemplate, setShowTemplate] = useState(false);

  // Trip type options
  const tripTypes = [
    { value: "leisure", label: "Leisure" },
    { value: "business", label: "Business" },
    { value: "adventure", label: "Adventure" },
    { value: "cultural", label: "Cultural" },
  ];

  // Handle form field changes
  const handleChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
    // Clear messages when user types
    if (error) setError("");
    if (success) setSuccess("");
  };

  // Validate form data
  const validateForm = () => {
    const errors = [];

    if (!formData.destination.trim()) {
      errors.push("Destination is required");
    }
    if (!formData.startDate) {
      errors.push("Start date is required");
    }
    if (!formData.endDate) {
      errors.push("End date is required");
    }
    if (formData.startDate && formData.endDate) {
      const startDate = new Date(formData.startDate);
      const endDate = new Date(formData.endDate);
      if (endDate <= startDate) {
        errors.push("End date must be after start date");
      }
      if (startDate < new Date().setHours(0, 0, 0, 0)) {
        errors.push("Start date cannot be in the past");
      }
    }

    return errors;
  };

  // Generate itinerary template
  const handleGenerateTemplate = async () => {
    if (!formData.destination || !formData.startDate || !formData.endDate) {
      setError("Please fill in destination and dates first");
      return;
    }

    try {
      setLoading(true);
      const response = await tripsAPI.getTemplate({
        destination: formData.destination,
        start_date: formData.startDate,
        end_date: formData.endDate,
        trip_type: formData.tripType,
      });

      setGeneratedTemplate(response.data.template);
      setShowTemplate(true);
      setSuccess("Template generated! You can edit it below or use as-is.");
    } catch (err) {
      console.error("Template generation error:", err);
      setError(
        "Failed to generate template. You can still create a trip manually."
      );
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Validate form
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setError(validationErrors.join(", "));
      setLoading(false);
      return;
    }

    try {
      // Prepare trip data
      const tripData = {
        destination: formData.destination.trim(),
        start_date: formData.startDate,
        end_date: formData.endDate,
      };

      // Add coordinates if provided
      if (formData.latitude && formData.longitude) {
        tripData.latitude = parseFloat(formData.latitude);
        tripData.longitude = parseFloat(formData.longitude);
      }

      // Add itinerary - use template or custom
      if (generatedTemplate && showTemplate) {
        tripData.itinerary = generatedTemplate.itinerary;
      } else if (formData.customItinerary.trim()) {
        // Try to parse as JSON, fallback to simple text
        try {
          tripData.itinerary = JSON.parse(formData.customItinerary);
        } catch {
          tripData.itinerary = { notes: formData.customItinerary.trim() };
        }
      }

      // Create trip via API
      const response = await tripsAPI.createTrip(tripData);

      setSuccess("Trip created successfully! Redirecting to dashboard...");

      // Navigate to dashboard after 2 seconds
      setTimeout(() => {
        navigate("/dashboard");
      }, 2000);
    } catch (err) {
      console.error("Trip creation error:", err);
      setError(
        err.response?.data?.error || "Failed to create trip. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        {/* Header */}
        <Box display="flex" alignItems="center" mb={4}>
          <Flight sx={{ fontSize: 40, color: "primary.main", mr: 2 }} />
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              Create New Trip
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              Plan your next adventure, {user?.email_address?.split("@")[0]}!
            </Typography>
          </Box>
        </Box>

        {/* Messages */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            {success}
          </Alert>
        )}

        {/* Form */}
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Destination */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Destination"
                placeholder="e.g., Paris, France"
                value={formData.destination}
                onChange={(e) => handleChange("destination", e.target.value)}
                required
                InputProps={{
                  startAdornment: (
                    <LocationOn sx={{ mr: 1, color: "action.active" }} />
                  ),
                }}
              />
            </Grid>

            {/* Dates - Using regular text inputs with date type */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                value={formData.startDate}
                onChange={(e) => handleChange("startDate", e.target.value)}
                required
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  min: new Date().toISOString().split("T")[0],
                }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="End Date"
                type="date"
                value={formData.endDate}
                onChange={(e) => handleChange("endDate", e.target.value)}
                required
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  min:
                    formData.startDate ||
                    new Date().toISOString().split("T")[0],
                }}
              />
            </Grid>

            {/* Trip Type */}
            <Grid item xs={12} sm={6}>
              <TextField
                select
                fullWidth
                label="Trip Type"
                value={formData.tripType}
                onChange={(e) => handleChange("tripType", e.target.value)}
              >
                {tripTypes.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Generate Template Button */}
            <Grid item xs={12} sm={6}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<AutoAwesome />}
                onClick={handleGenerateTemplate}
                disabled={
                  loading ||
                  !formData.destination ||
                  !formData.startDate ||
                  !formData.endDate
                }
                sx={{ height: "56px" }}
              >
                Generate Itinerary
              </Button>
            </Grid>

            {/* Coordinates (Optional) */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Optional Details
                </Typography>
              </Divider>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Latitude"
                placeholder="e.g., 48.8566"
                value={formData.latitude}
                onChange={(e) => handleChange("latitude", e.target.value)}
                type="number"
                inputProps={{ step: "any" }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Longitude"
                placeholder="e.g., 2.3522"
                value={formData.longitude}
                onChange={(e) => handleChange("longitude", e.target.value)}
                type="number"
                inputProps={{ step: "any" }}
              />
            </Grid>

            {/* Generated Template Display */}
            {showTemplate && generatedTemplate && (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, bgcolor: "grey.50" }}>
                  <Typography variant="h6" gutterBottom>
                    Generated Itinerary Preview
                  </Typography>
                  <Typography
                    variant="body2"
                    color="textSecondary"
                    gutterBottom
                  >
                    This itinerary will be saved with your trip
                  </Typography>
                  <Box sx={{ maxHeight: 200, overflow: "auto" }}>
                    <pre style={{ whiteSpace: "pre-wrap", fontSize: "12px" }}>
                      {JSON.stringify(generatedTemplate.itinerary, null, 2)}
                    </pre>
                  </Box>
                  <Button
                    size="small"
                    onClick={() => setShowTemplate(false)}
                    sx={{ mt: 1 }}
                  >
                    Use Custom Instead
                  </Button>
                </Paper>
              </Grid>
            )}

            {/* Custom Itinerary */}
            {!showTemplate && (
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Custom Itinerary (Optional)"
                  placeholder="Enter your trip itinerary as JSON or simple text"
                  value={formData.customItinerary}
                  onChange={(e) =>
                    handleChange("customItinerary", e.target.value)
                  }
                  helperText="You can write simple text or JSON format"
                />
              </Grid>
            )}

            {/* Submit Buttons */}
            <Grid item xs={12}>
              <Box display="flex" gap={2} justifyContent="flex-end">
                <Button
                  variant="outlined"
                  onClick={() => navigate("/dashboard")}
                  disabled={loading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={
                    loading ? <CircularProgress size={20} /> : <Save />
                  }
                  disabled={loading}
                >
                  {loading ? "Creating..." : "Create Trip"}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Container>
  );
};

export default CreateTripPage;
