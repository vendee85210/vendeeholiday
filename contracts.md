# Pure France Backend Implementation Contracts

## API Endpoints & Data Models

### 1. Authentication & Users
**Endpoints:**
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout
- GET /api/auth/profile - Get user profile
- PUT /api/auth/profile - Update user profile

**Models:**
- User: id, email, first_name, last_name, phone, password_hash, role (guest/owner/admin), created_at
- Session: id, user_id, token, expires_at

### 2. Properties Management
**Endpoints:**
- GET /api/properties - List all properties (with filters)
- GET /api/properties/{id} - Get single property
- POST /api/properties - Create new property (owners only)
- PUT /api/properties/{id} - Update property (owners only)
- DELETE /api/properties/{id} - Delete property (owners only)
- GET /api/properties/search - Advanced search with filters

**Models:**
- Property: id, owner_id, name, description, bedrooms, bathrooms, max_guests, property_type, region, address, latitude, longitude, price_per_night, images[], amenities[], availability[], created_at, updated_at
- PropertyImage: id, property_id, url, alt_text, is_primary
- Amenity: id, name, icon, category

### 3. Destinations
**Endpoints:**
- GET /api/destinations - List all destinations
- GET /api/destinations/{slug} - Get destination details
- GET /api/destinations/{slug}/properties - Properties in destination

**Models:**
- Destination: id, name, slug, description, image_url, region_type, featured, created_at

### 4. Bookings
**Endpoints:**
- POST /api/bookings - Create new booking
- GET /api/bookings - List user's bookings
- GET /api/bookings/{id} - Get booking details
- PUT /api/bookings/{id} - Update booking
- DELETE /api/bookings/{id} - Cancel booking
- POST /api/bookings/{id}/payment - Process payment

**Models:**
- Booking: id, user_id, property_id, check_in, check_out, guests, total_price, status (pending/confirmed/cancelled), payment_status, special_requests, created_at
- Payment: id, booking_id, amount, payment_method, transaction_id, status, processed_at

### 5. Blog & Content
**Endpoints:**
- GET /api/blog/posts - List blog posts
- GET /api/blog/posts/{slug} - Get single blog post
- GET /api/inspiration - Get inspiration categories
- GET /api/special-offers - Get current special offers

**Models:**
- BlogPost: id, title, slug, excerpt, content, featured_image, author_id, published, published_at, created_at
- InspirationCategory: id, title, slug, description, image_url, property_count
- SpecialOffer: id, title, description, discount_percentage, valid_from, valid_until, property_ids[], active

### 6. Reviews & Ratings
**Endpoints:**
- GET /api/properties/{id}/reviews - Get property reviews
- POST /api/properties/{id}/reviews - Add review (authenticated users only)
- GET /api/reviews/{id} - Get single review
- PUT /api/reviews/{id} - Update review (author only)
- DELETE /api/reviews/{id} - Delete review (author/admin only)

**Models:**
- Review: id, user_id, property_id, booking_id, rating, title, content, created_at, updated_at

## Frontend Integration Plan

### Replace Mock Data:
1. **destinations** from mock/data.js → API call to /api/destinations
2. **properties** from mock/data.js → API call to /api/properties
3. **blogPosts** from mock/data.js → API call to /api/blog/posts
4. **inspirationCategories** from mock/data.js → API call to /api/inspiration

### Add New Features:
1. **User Authentication** - Login/Register forms with session management
2. **Property Search** - Real search functionality with filters
3. **Booking System** - Complete booking flow with payment
4. **User Dashboard** - Manage bookings, profile, reviews
5. **Owner Portal** - Property management interface
6. **Admin Panel** - Content and user management

### Component Updates Needed:
- **Header.jsx**: Add login/logout functionality, user menu
- **Hero.jsx**: Connect search form to real API
- **Destinations.jsx**: Fetch from API, add property counts
- **LatestProperties.jsx**: Real-time property data
- **Blog.jsx**: Dynamic blog content
- **Add new components**: LoginForm, BookingForm, UserDashboard, PropertyDetails

## Database Schema

### Collections:
1. **users** - User accounts and authentication
2. **properties** - Holiday rental properties
3. **destinations** - French regions and areas
4. **bookings** - Reservation records
5. **blog_posts** - Blog content
6. **reviews** - Property reviews and ratings
7. **special_offers** - Promotional campaigns
8. **sessions** - User session management

## Security & Validation
- JWT authentication for protected routes
- Input validation and sanitization
- Rate limiting on search and booking endpoints
- Owner verification for property operations
- Secure password hashing with bcrypt
- CORS configuration for frontend integration

## Business Logic
- **Availability checking** - Prevent double bookings
- **Dynamic pricing** - Seasonal rates and special offers
- **Search algorithms** - Location, amenities, availability matching
- **Email notifications** - Booking confirmations, reminders
- **Payment processing** - Integration with payment gateway
- **Review moderation** - Content filtering and approval workflow

This implementation will transform the frontend-only demo into a fully functional holiday rental platform matching Pure France's capabilities.