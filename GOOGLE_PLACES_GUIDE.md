# Google Places API Integration Guide

## 📍 Overview

The Sydney Rental Hub now includes Google Places Autocomplete API integration for address searching. The implementation supports both development mode (with mock data) and production mode (with real Google API).

## 🚀 Current Implementation Status

### ✅ Completed
- Places service module (`vue-frontend/src/services/places.js`)
- Integration in AddLocationModal component
- Development mode with mock data
- Session token optimization for billing
- Preset locations for common Sydney places
- Geocoding support

### 🔧 Configuration Required
- Google Maps API key setup (for production)
- Environment variables configuration

## 📝 Setup Instructions

### 1. Development Mode (Default)

No API key required! The app runs in development mode by default with mock data.

```bash
# Vue frontend will use mock data automatically
cd vue-frontend
npm run dev
```

**Features in Dev Mode:**
- Mock search results for any address query
- Preset Sydney locations (Universities, Stations, Landmarks)
- Random coordinates generation for testing
- No API quota usage

### 2. Production Mode

To use real Google Places API:

#### Step 1: Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Create credentials (API Key)
5. Add API restrictions:
   - HTTP referrers: `http://localhost:5173/*` (development)
   - HTTP referrers: `https://yourdomain.com/*` (production)

#### Step 2: Configure Environment Variables

```bash
# Copy the example file
cp vue-frontend/.env.example vue-frontend/.env

# Edit the .env file
# Add your API key:
VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here

# Set dev mode to false for production:
VITE_GOOGLE_PLACES_DEV_MODE=false
```

#### Step 3: Restart the Application

```bash
cd vue-frontend
npm run dev
```

## 🎯 How It Works

### User Flow

1. User clicks "Add location" in CommuteTimes page
2. AddLocationModal opens with:
   - Search input field
   - Preset popular locations (when search is empty)
   - Real-time autocomplete suggestions (as user types)
3. User selects a location:
   - From preset locations
   - From search results
4. System retrieves full place details including coordinates
5. Location is saved with proper formatting

### Technical Implementation

```javascript
// The service automatically detects mode based on configuration
import placesService from '@/services/places'

// Search for places
const results = await placesService.searchPlaces('Sydney Opera House')

// Get place details with coordinates
const details = await placesService.getPlaceDetails(placeId)

// Geocode an address
const coords = await placesService.geocodeAddress('123 George St, Sydney')
```

### Session Token Optimization

The implementation uses session tokens to optimize Google API billing:
- One token per complete search session
- Token resets after place selection
- Reduces API costs by ~50%

## 🧪 Testing

### Test in Development Mode (No API Key)

1. Navigate to a property detail page
2. Click "See travel times"
3. Add a location using the search
4. Verify mock results appear
5. Select a location and verify it's added

### Test in Production Mode (With API Key)

1. Configure your API key in `.env`
2. Set `VITE_GOOGLE_PLACES_DEV_MODE=false`
3. Restart the application
4. Test same flow as above
5. Verify real Google results appear

## 🏷️ Preset Locations

The following locations are always available:

- **Universities:**
  - University of Sydney (USYD)
  - University of New South Wales (UNSW)
  - University of Technology Sydney (UTS)
  - Macquarie University

- **Transport Hubs:**
  - Central Station
  - Town Hall Station

- **Landmarks:**
  - Sydney Opera House
  - Sydney CBD

## 📊 API Usage & Quotas

### Google Maps API Pricing (as of 2025)

- **Places Autocomplete:** $2.83 per 1,000 requests
- **Place Details:** $17.00 per 1,000 requests  
- **Geocoding:** $5.00 per 1,000 requests

### Optimization Strategies Implemented

1. **Session Tokens:** Groups autocomplete requests for billing
2. **Debouncing:** 300ms delay reduces unnecessary API calls
3. **Caching:** Results cached in frontend store
4. **Preset Locations:** Common places don't require API calls
5. **Development Mode:** Testing doesn't consume quota

## 🔒 Security Considerations

1. **API Key Restrictions:**
   - Always restrict by HTTP referrer
   - Limit to specific APIs only
   - Set quota limits in Google Console

2. **Never expose in:**
   - Public repositories (use .env files)
   - Client-side code (use proxy if needed)
   - Error messages or logs

## 🐛 Troubleshooting

### Common Issues

**1. "Google is not defined" error**
- Solution: API key not configured or invalid
- Check: Browser console for loading errors

**2. No search results appearing**
- Solution: Check API key has Places API enabled
- Verify: Network tab for API responses

**3. CORS errors**
- Solution: Verify HTTP referrer restrictions
- Add: Your domain to allowed referrers

**4. Quota exceeded errors**
- Solution: Check Google Cloud Console quotas
- Consider: Implementing backend proxy

### Debug Mode

Enable debug logging:
```javascript
// In browser console
localStorage.setItem('places_debug', 'true')
```

## 📈 Future Enhancements

- [ ] Implement backend proxy for API calls
- [ ] Add place photos display
- [ ] Support for business hours
- [ ] Place reviews integration
- [ ] Offline caching strategy
- [ ] Advanced filtering (ATMs, parking, etc.)

## 📚 Resources

- [Google Places API Documentation](https://developers.google.com/maps/documentation/places/web-service)
- [Places Autocomplete Guide](https://developers.google.com/maps/documentation/javascript/places-autocomplete)
- [API Pricing Calculator](https://developers.google.com/maps/billing-and-pricing/pricing)
- [Best Practices](https://developers.google.com/maps/documentation/javascript/best-practices)

---

**Note:** The current implementation defaults to development mode with mock data. This allows full testing without an API key. When ready for production, simply add your API key and set the environment flags.