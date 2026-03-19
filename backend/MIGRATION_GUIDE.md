# Chatify Backend Migration Guide: Node.js to Python

## Overview

The Chatify backend has been successfully migrated from Node.js (Express) to Python (FastAPI). This document outlines the changes, setup instructions, and how to ensure all functionality works correctly.

## What Was Changed

### Frontend Compatibility ✅

The API endpoints remain **exactly the same** - no frontend changes required:

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `PUT /api/auth/update-profile`
- `GET /api/auth/check`
- `GET /api/messages/contacts`
- `GET /api/messages/{id}`
- `POST /api/messages/send/{id}`
- `GET /api/messages/chat-partners`

### Technology Stack Changes

| Feature          | Node.js                 | Python                       |
| ---------------- | ----------------------- | ---------------------------- |
| Framework        | Express.js              | FastAPI                      |
| Database Driver  | Mongoose                | Motor (async)                |
| Authentication   | custom middleware + JWT | FastAPI dependencies + PyJWT |
| Password Hashing | bcryptjs                | bcrypt                       |
| Email Service    | Resend (v1)             | Resend (custom HTTP client)  |
| Image Upload     | cloudinary-js           | cloudinary-python            |
| Real-time        | Socket.IO               | Socket.IO (prepared)         |

### Architecture

```
backend/
├── pyproject.toml          # uv project configuration
├── .env                    # Environment variables
├── README.md               # Setup documentation
├── src/
│   ├── server.py           # FastAPI app entry point
│   ├── models/             # Pydantic data models
│   │   ├── User.py         # User model
│   │   └── Message.py      # Message model
│   ├── controllers/        # Business logic
│   │   ├── auth_controller.py
│   │   └── message_controller.py
│   ├── routes/             # API endpoints
│   │   ├── auth_route.py
│   │   └── message_route.py
│   ├── middleware/         # FastAPI middleware
│   │   └── auth_middleware.py
│   ├── lib/                # Utilities
│   │   ├── config.py       # Configuration loader
│   │   ├── db.py           # MongoDB connection (Motor)
│   │   ├── utils.py        # JWT helpers
│   │   ├── cloudinary.py   # Image upload
│   │   ├── resend.py       # Email sending
│   │   └── socket.py       # Socket.IO manager
│   └── emails/             # Email templates
│       ├── email_handlers.py
│       └── email_templates.py
└── tests/                  # Test files (TBD)
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- MongoDB (local or Atlas)
- uv package manager

### 2. Install Dependencies

```bash
cd backend
uv sync
```

This will:

- Create a virtual environment
- Install all dependencies from pyproject.toml
- Set up dev dependencies

### 3. Configure Environment Variables

```bash
# Copy the .env file and update with your values
cat .env

# Update these critical values:
# - MONGO_URI: Your MongoDB connection string
# - JWT_SECRET: A secure secret key
# - CLOUDINARY_*: Your Cloudinary credentials
# - RESEND_API_KEY: Your Resend email API key
# - CLIENT_URL: Your frontend URL (default: http://localhost:5173)
```

### 4. Start the Server

**Development mode (with auto-reload):**

```bash
uv run uvicorn src.server:app --reload --host 0.0.0.0 --port 3000
```

**Production mode:**

```bash
uv run uvicorn src.server:app --host 0.0.0.0 --port 3000 --workers 4
```

The server will be available at `http://localhost:3000`

## API Compatibility Testing

All endpoints have been preserved. Test them with:

```bash
# Health check
curl http://localhost:3000/api/health

# Signup
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","fullName":"User","password":"123456"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"123456"}' \
  -c cookies.txt

# Protected endpoint (with JWT cookie)
curl http://localhost:3000/api/auth/check -b cookies.txt
```

## Key Implementation Details

### Authentication

- JWT tokens are stored in **httpOnly cookies** (same as Node.js)
- Token expiration: 7 days
- Password hashing: bcrypt with 10 rounds (same as Node.js)

### Database

- **Motor** provides async MongoDB operations
- All database calls are awaited (async/await pattern)
- ObjectId conversion between MongoDB and JSON responses handled

### Email Sending

- Uses Resend API with custom HTTP client
- Welcome emails sent on signup (if API key configured)
- Failures don't block user creation

### Image Upload

- Cloudinary integration preserved
- Base64 images converted and uploaded
- Secure URLs returned

### Error Handling

- Consistent error response format matches Node.js backend
- Standard HTTP status codes (400, 401, 404, 500)
- Detailed error logging to console

## Migration Verification Checklist

- [x] Database connection with Motor
- [x] Authentication endpoints (signup, login, logout)
- [x] User profile management
- [x] Message sending and retrieval
- [x] Contact list endpoints
- [x] Chat partner list endpoint
- [x] JWT token generation and validation
- [x] Password hashing with bcrypt
- [x] CORS configuration matching frontend
- [x] Cookie-based JWT storage
- [x] Cloudinary image uploads
- [x] Email sending framework
- [ ] Socket.IO real-time communication (prepared, needs WebSocket setup)
- [ ] Comprehensive test suite

## Known Differences from Node.js

1. **Real-time Messaging**: Socket.IO support is prepared but not fully integrated. Currently, messages are stored and retrieved via REST API. To add Socket.IO:
   - Install: `uv pip install python-socketio python-engineio`
   - Use `starlette-socketio` or implement WebSocket endpoints
   - Update message delivery to emit real-time events

2. **Rate Limiting**: Arcjet integration is not currently implemented. Options:
   - Add fastapi-limiter dependency
   - Use Redis for rate limiting
   - Implement Arcjet Python SDK

3. **Async Operations**: All database operations are async/await, providing better concurrency than the Node.js version

## Environment Variables

```
# Server
PORT=3000
NODE_ENV=development
CLIENT_URL=http://localhost:5173

# Database
MONGO_URI=mongodb://localhost:27017/chatify

# Authentication
JWT_SECRET=your_super_secret_key_change_in_production

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Email (Resend)
RESEND_API_KEY=your_resend_api_key
EMAIL_FROM=noreply@chatify.com
EMAIL_FROM_NAME=Chatify

# Rate Limiting (optional)
ARCJET_KEY=your_arcjet_key
ARCJET_ENV=development
```

## Performance Benefits

The Python backend offers several performance advantages:

1. **Async Operations**: All I/O operations (DB, HTTP) are truly async
2. **Concurrent Requests**: Better handling of simultaneous connections
3. **Memory Efficient**: Python processes use less memory than Node.js for similar workloads
4. **Type Safety**: FastAPI with Pydantic provides runtime type validation

## Troubleshooting

### Server won't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
uv sync --verbose

# Test MongoDB connection
uv run python -c "from src.lib.config import config; print(config.MONGO_URI)"
```

### Database connection fails

```bash
# Ensure MongoDB is running
mongosh # Test connection

# Update MONGO_URI in .env
MONGO_URI=mongodb://localhost:27017/chatify
```

### Email sending fails

```bash
# Check Resend API key
RESEND_API_KEY=re_xxxxxxxxxxxxx  # Must start with 're_'

# Test email sending (check server logs)
# It won't block signup even if email fails
```

## Next Steps / TODO

1. **Socket.IO Integration**: Implement real-time messaging
   - Add `starlette-socketio` or use FastAPI WebSockets
   - Connect to existing Socket.IO client in frontend

2. **Rate Limiting**: Restore Arcjet protection
   - Implement fastapi-limiter
   - Or use Arcjet Python SDK

3. **Testing**: Create comprehensive test suite
   - Unit tests for controllers
   - Integration tests for APIs
   - Use pytest and pytest-asyncio

4. **Monitoring**: Add logging and monitoring
   - Structured logging (e.g., Structlog)
   - Error tracking (e.g., Sentry)

5. **Production Deployment**:
   - Use `gunicorn` with uvicorn workers
   - Set `secure=true` in JWT cookie
   - Configure proper CORS for production domain
   - Add SSL/TLS certificates

## Support

For issues or questions about the migration:

1. Check the server logs for detailed error messages
2. Verify environment configuration in `.env`
3. Ensure MongoDB is running and accessible
4. Test API endpoints with curl or Postman

---

**Migration Date**: March 19, 2026  
**Backend Type**: Python/FastAPI  
**Previous Backend**: Node.js/Express  
**Status**: ✅ Core functionality working
