import React, { useState, useEffect } from 'react';
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
  Breadcrumbs,
  Link,
} from '@mui/material';
import {
  Flight,
  LocationOn,
  Save,
  AutoAwesome,
  ArrowBack,
  Home,
} from '@mui/icons-material';
import { tripsAPI } from '../services/api';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const EditTripPage = () => {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  // Form state
  const [formData, setFormData] = useState({
    destination: '',
    startDate: '',
    endDate: '',
    latitude: '',
    longitude: '',
    tripType: 'leisure',
    customItinerary: '',
  });

  // UI state
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [originalTrip, setOriginalTrip] = useState(null);
  const [generatedTemplate, setGeneratedTemplate] = useState(null);
  const [showTemplate, setShowTemplate] = useState(false);

  // Trip type options
  const tripTypes = [
    { value: 'leisure', label: 'Leisure' },
    { value: 'business', label: 'Business' },
    { value: 'adventure', label: 'Adventure' },
    { value: 'cultural', label: 'Cultural' },
  ];

  // Fetch trip data when component loads
  useEffect(() => {
    fetchTripData();
  }, [tripId]);

  const fetchTripData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await tripsAPI.getTrip(tripId);
      const trip = response.data.trip;
      
      // Store original trip data
      setOriginalTrip(trip);
      
      // Populate form with existing data
      setFormData({
        destination: trip.destination || '',
        startDate: trip.start_date || '',
        endDate: trip.end_date || '',
        latitude: trip.coordinates?.latitude?.toString() || '',
        longitude: trip.coordinates?.longitude?.toString() || '',
        tripType: 'leisure', // Default since we don't store trip type
        customItinerary: trip.itinerary ? (
          typeof trip.itinerary === 'string' ? trip.itinerary : JSON.stringify(trip.itinerary, null, 2)
        ) : '',
      });
    } catch (err) {
      console.error('Error fetching trip:', err);
      if (err.response?.status === 404) {
        setError('Trip not found or you do not have permission to edit it.');
      } else {
        setError('Failed to load trip data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Handle form field changes
  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    // Clear messages when user types
    if (error) setError('');
    if (success) setSuccess('');
  };

  // Validate form data
  const validateForm = () => {
    const errors = [];

    if (!formData.destination.trim()) {
      errors.push('Destination is required');
    }
    if (!formData.startDate) {
      errors.push('Start date is required');
    }
    if (!formData.endDate) {
      errors.push('End date is required');
    }
    if (formData.startDate && formData.endDate) {
      const startDate = new Date(formData.startDate);
      const endDate = new Date(formData.endDate);
      if (endDate <= startDate) {
        errors.push('End date must be after start date');
      }
    }

    return errors;
  };

  // Generate itinerary template
  const handleGenerateTemplate = async () => {
    if (!formData.destination || !formData.startDate || !formData.endDate) {
      setError('Please fill in destination and dates first');
      return;
    }

    try {
      setSaving(true);
      const response = await tripsAPI.getTemplate({
        destination: formData.destination,
        start_date: formData.startDate,
        end_date: formData.endDate,
        trip_type: formData.tripType,
      });

      setGeneratedTemplate(response.data.template);
      setShowTemplate(true);
      setSuccess('Template generated! You can edit it below or use as-is.');
    } catch (err) {
      console.error('Template generation error:', err);
      setError('Failed to generate template. You can still edit the trip manually.');
    } finally {
      setSaving(false);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');

    // Validate form
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setError(validationErrors.join(', '));
      setSaving(false);
      return;
    }

    try {
      // Prepare trip data (only send changed fields)
      const tripData = {};
      
      if (formData.destination !== originalTrip.destination) {
        tripData.destination = formData.destination.trim();
      }
      if (formData.startDate !== originalTrip.start_date) {
        tripData.start_date = formData.startDate;
      }
      if (formData.endDate !== originalTrip.end_date) {
        tripData.end_date = formData.endDate;
      }

      // Handle coordinates
      const currentLat = originalTrip.coordinates?.latitude?.toString() || '';
      const currentLng = originalTrip.coordinates?.longitude?.toString() || '';
      
      if (formData.latitude !== currentLat || formData.longitude !== currentLng) {
        if (formData.latitude && formData.longitude) {
          tripData.latitude = parseFloat(formData.latitude);
          tripData.longitude = parseFloat(formData.longitude);
        } else {
          tripData.latitude = null;
          tripData.longitude = null;
        }
      }

      // Handle itinerary
      let newItinerary = null;
      if (generatedTemplate && showTemplate) {
        newItinerary = generatedTemplate.itinerary;
      } else if (formData.customItinerary.trim()) {
        try {
          newItinerary = JSON.parse(formData.customItinerary);
        } catch {
          newItinerary = { notes: formData.customItinerary.trim() };
        }
      }

      const originalItineraryStr = originalTrip.itinerary ? 
        (typeof originalTrip.itinerary === 'string' ? originalTrip.itinerary : JSON.stringify(originalTrip.itinerary)) : '';
      const newItineraryStr = newItinerary ? JSON.stringify(newItinerary) : '';
      
      if (newItineraryStr !== originalItineraryStr) {
        tripData.itinerary = newItinerary;
      }

      // Only make API call if there are changes
      if (Object.keys(tripData).length === 0) {
        setError('No changes detected');
        setSaving(false);
        return;
      }

      // Update trip via API
      await tripsAPI.updateTrip(tripId, tripData);

      setSuccess('Trip updated successfully! Redirecting...');
      
      // Navigate to trip details after 2 seconds
      setTimeout(() => {
        navigate(`/trips/${tripId}`);
      }, 2000);

    } catch (err) {
      console.error('Trip update error:', err);
      setError(err.response?.data?.error || 'Failed to update trip. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  // Loading state
  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  // Error state (if couldn't load trip)
  if (error && !originalTrip) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
        >
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link
          color="inherit"
          href="#"
          onClick={() => navigate('/')}
          sx={{ display: 'flex', alignItems: 'center' }}
        >
          <Home sx={{ mr: 0.5 }} fontSize="inherit" />
          Home
        </Link>
        <Link color="inherit" href="#" onClick={() => navigate('/dashboard')}>
          Dashboard
        </Link>
        <Link color="inherit" href="#" onClick={() => navigate(`/trips/${tripId}`)}>
          Trip Details
        </Link>
        <Typography color="text.primary">Edit Trip</Typography>
      </Breadcrumbs>

      <Paper elevation={3} sx={{ p: 4 }}>
        {/* Header */}
        <Box display="flex" alignItems="center" mb={4}>
          <Flight sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              Edit Trip
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              Update your trip to {originalTrip?.destination}, {user?.email_address?.split('@')[0]}!
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
                onChange={(e) => handleChange('destination', e.target.value)}
                required
                InputProps={{
                  startAdornment: <LocationOn sx={{ mr: 1, color: 'action.active' }} />,
                }}
              />
            </Grid>

            {/* Dates */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                value={formData.startDate}
                onChange={(e) => handleChange('startDate', e.target.value)}
                required
                InputLabelProps={{ shrink: true }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="End Date"
                type="date"
                value={formData.endDate}
                onChange={(e) => handleChange('endDate', e.target.value)}
                required
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  min: formData.startDate || new Date().toISOString().split('T')[0],
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
                onChange={(e) => handleChange('tripType', e.target.value)}
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
                disabled={saving || !formData.destination || !formData.startDate || !formData.endDate}
                sx={{ height: '56px' }}
              >
                Regenerate Itinerary
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
                onChange={(e) => handleChange('latitude', e.target.value)}
                type="number"
                inputProps={{ step: 'any' }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Longitude"
                placeholder="e.g., 2.3522"
                value={formData.longitude}
                onChange={(e) => handleChange('longitude', e.target.value)}
                type="number"
                inputProps={{ step: 'any' }}
              />
            </Grid>

            {/* Generated Template Display */}
            {showTemplate && generatedTemplate && (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                  <Typography variant="h6" gutterBottom>
                    Generated Itinerary Preview
                  </Typography>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    This will replace your current itinerary
                  </Typography>
                  <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                    <pre style={{ whiteSpace: 'pre-wrap', fontSize: '12px' }}>
                      {JSON.stringify(generatedTemplate.itinerary, null, 2)}
                    </pre>
                  </Box>
                  <Button
                    size="small"
                    onClick={() => setShowTemplate(false)}
                    sx={{ mt: 1 }}
                  >
                    Edit Custom Instead
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
                  rows={6}
                  label="Itinerary"
                  placeholder="Enter your trip itinerary as JSON or simple text"
                  value={formData.customItinerary}
                  onChange={(e) => handleChange('customItinerary', e.target.value)}
                  helperText="You can write simple text or JSON format"
                />
              </Grid>
            )}

            {/* Submit Buttons */}
            <Grid item xs={12}>
              <Box display="flex" gap={2} justifyContent="flex-end">
                <Button
                  variant="outlined"
                  onClick={() => navigate(`/trips/${tripId}`)}
                  disabled={saving}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={saving ? <CircularProgress size={20} /> : <Save />}
                  disabled={saving}
                >
                  {saving ? 'Updating...' : 'Update Trip'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Container>
  );
};

export default EditTripPage;
