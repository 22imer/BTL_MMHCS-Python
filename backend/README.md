# Python backend (FastAPI + async/await with Motor for async MongoDB)

## Setup

### Prerequisites

- Python 3.9+
- MongoDB
- uv package manager

### Installation

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment using uv:

```bash
uv venv
```

3. Activate the virtual environment:

```bash
# On Windows
.\.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
# or
uv sync
```

5. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Run the server:

```bash
# Development
uv run uvicorn src.server:app --reload --host 0.0.0.0 --port 3000

# Production
uv run uvicorn src.server:app --host 0.0.0.0 --port 3000
```

## Project Structure

```
src/
├── server.py           # FastAPI application entry point
├── models/             # Pydantic models (User, Message)
├── controllers/        # Business logic handlers
├── routes/             # API route handlers
├── middleware/         # Authentication and other middleware
├── lib/                # Utility functions (DB, JWT, etc.)
└── emails/             # Email templates and handlers
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `PUT /api/auth/update-profile` - Update user profile
- `GET /api/auth/check` - Check authentication status

### Messages

- `GET /api/messages/contacts` - Get all users
- `GET /api/messages/{id}` - Get messages with a specific user
- `POST /api/messages/send/{id}` - Send a message
- `GET /api/messages/chat-partners` - Get chat partners

## Real-time Features

The application uses Socket.IO for real-time messaging:

- User connection/disconnection status
- Real-time message delivery
- Online users list broadcasting

## Environment Variables

See `.env` file for required configuration:

- `MONGO_URI` - MongoDB connection string
- `JWT_SECRET` - JWT signing secret
- `CLIENT_URL` - Frontend URL for CORS
- `CLOUDINARY_*` - Cloudinary configuration
- `RESEND_API_KEY` - Resend email service API key
- `ARCJET_KEY` - Arcjet rate limiting service key

## Development

### Running Tests

```bash
uv run pytest tests/
```

### Linting

```bash
uv run flake8 src/
```

### Type Checking

```bash
uv run mypy src/
```

## Notes

- This is a Python/FastAPI port of the original Node.js/Express backend
- Uses Motor for async MongoDB operations
- JWT tokens are stored in httpOnly cookies
- Socket.IO is configured for async HTTP server (aiohttp)
- CORS is configured to allow requests from the frontend URL
