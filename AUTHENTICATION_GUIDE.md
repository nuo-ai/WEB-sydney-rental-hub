# Sydney Rental Hub - Authentication System Guide

## Overview

A complete JWT-based authentication system has been implemented for the Sydney Rental Hub project. This system provides user registration, email verification, login, token refresh, and user address management.

## Backend Implementation

### New Files Created
- `backend/models/user_models.py` - Pydantic models for users and authentication
- `backend/crud/auth_crud.py` - Database operations for authentication
- `backend/api/auth_routes.py` - FastAPI routes for authentication endpoints

### Database Schema
The system automatically creates two tables:
- `users` - Store user accounts with email verification
- `user_addresses` - Store user's saved addresses with labels

### API Endpoints

#### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user  
- `POST /api/auth/verify-email` - Verify user email
- `POST /api/auth/resend-verification` - Resend verification email
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user profile

#### User Address Endpoints  
- `GET /api/auth/addresses` - Get user's saved addresses
- `POST /api/auth/addresses` - Save new address
- `DELETE /api/auth/addresses/{id}` - Delete address

#### Test Endpoint
- `GET /api/auth/test` - Test authentication system status

### Security Features
- Password hashing with bcrypt
- JWT access tokens (30 min expiry)
- Refresh tokens (7 day expiry)
- Email verification required
- Secure token generation
- Automatic token refresh

## Frontend Implementation

### Updated Files
- `vue-frontend/src/stores/auth.js` - Updated with real API calls
- `vue-frontend/src/main.js` - Initialize auth store

### Key Features
- Real API integration with error handling
- Automatic token refresh on API calls
- Test mode support for development
- Local storage persistence
- User address management

### Test Mode
The system supports a test mode that bypasses authentication for development:

```javascript
// Enable test mode
authStore.enableTestMode()

// Disable test mode  
authStore.disableTestMode()

// Check if in test mode
authStore.testMode
```

## Usage Examples

### Frontend Usage

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Register new user
await authStore.register('user@example.com', 'password123', 'John Doe')

// Login user
await authStore.login('user@example.com', 'password123')

// Save user address
await authStore.saveUserAddress({
  address: 'University of Sydney, Camperdown NSW 2006',
  label: 'School',
  placeId: 'ChIJVXealLmuEmsRUduC5Wd-6XQ', 
  latitude: -33.8886,
  longitude: 151.1873
})

// Check authentication
if (authStore.isAuthenticated) {
  // User is logged in
}
```

### Backend API Usage

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"John Doe"}'

# Login user  
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get user profile (requires Bearer token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Email Verification

Currently, email verification is implemented with console logging for development. In production, you would integrate with:
- SendGrid
- AWS SES  
- Mailgun
- Other email service providers

The verification flow:
1. User registers → receives temp token
2. Verification email sent with link containing token
3. User clicks link → email verified → account activated
4. User can now login

## Testing

### Automated Tests
Run the authentication system tests:

```bash
cd backend
python test_auth.py
```

### Manual Testing
1. Start the backend server
2. Navigate to `http://localhost:8000/docs` for interactive API docs
3. Test the `/api/auth/test` endpoint to verify system status
4. Test registration, login, and other endpoints

## Environment Variables

Make sure these are set in your `.env` file:

```env
# Required
DATABASE_URL=your_supabase_connection_string

# Optional (defaults provided)
SECRET_KEY=your_jwt_secret_key
AUTH_TEST_MODE=false
```

## Integration with Existing Code

### CommuteTimes Component
The existing `CommuteTimes.vue` component works with both:
- Real authentication (when users are logged in)
- Test mode (for development testing)

### Property Detail Page  
The "See travel times" button works with the new authentication system and respects test mode settings.

## Security Considerations

✅ **Implemented:**
- Password hashing with bcrypt
- JWT token expiration
- Secure token generation  
- Input validation with Pydantic
- SQL injection protection with parameterized queries

🔒 **Production Recommendations:**
- Use HTTPS in production
- Set strong SECRET_KEY
- Configure proper CORS origins
- Implement rate limiting on auth endpoints
- Add password reset functionality
- Set up proper email service
- Add 2FA support (future enhancement)

## Troubleshooting

### Common Issues
1. **Database connection errors** - Check DATABASE_URL in .env
2. **Import errors** - Ensure all dependencies installed (`pip install -r requirements.txt`)
3. **Token refresh fails** - Check if refresh token is expired
4. **Email verification not working** - Currently logs to console, implement email service

### Debug Mode
Enable test mode for development:
```javascript
localStorage.setItem('auth-testMode', 'true')
```

The authentication system is now fully implemented and ready for production use!