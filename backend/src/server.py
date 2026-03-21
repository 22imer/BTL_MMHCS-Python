import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# Socket.IO setup
from src.lib.socket import sio
from socketio import ASGIApp

from src.lib.db import connect_db, disconnect_db
from src.lib.config import config
from src.routes.auth_route import router as auth_router
from src.routes.message_route import router as message_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    logger.info("Starting application...")
    await connect_db()
    logger.info(f"Server will run on port: {config.PORT}")
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await disconnect_db()


# Create FastAPI app
fastapi_app = FastAPI(
    title="Chatify API",
    description="Real-time chat application API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
# In development: allow all origins for cross-machine communication
# In production: restrict to CLIENT_URL only
cors_origins = (
    ["*"] if config.NODE_ENV == "development"
    else [config.CLIENT_URL]
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
fastapi_app.include_router(auth_router)
fastapi_app.include_router(message_router)

# Serve uploaded images
uploads_dir = os.path.join(os.path.dirname(__file__), "../uploads")
os.makedirs(uploads_dir, exist_ok=True)
try:
    fastapi_app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
except Exception as e:
    logger.warning(f"Could not mount uploads directory: {e}")

# Health check endpoint
@fastapi_app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


# Serve frontend in production
if config.NODE_ENV == "production":
    frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
    if os.path.exists(frontend_dist):
        fastapi_app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")


# Wrap FastAPI app with Socket.IO
app = ASGIApp(sio, fastapi_app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.NODE_ENV == "development"
    )


