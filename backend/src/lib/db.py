from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import asyncio
from src.lib.config import config

# Global database instance
db: AsyncIOMotorDatabase = None
client: AsyncIOMotorClient = None

async def connect_db():
    """Connect to MongoDB database"""
    global db, client
    try:
        client = AsyncIOMotorClient(config.MONGO_URI)
        db = client.chatify
        # Test connection
        await db.command("ping")
        print(f"MONGODB CONNECTED: {client.address}")
    except Exception as error:
        print(f"Error connecting to MONGODB: {error}")
        raise

async def disconnect_db():
    """Disconnect from MongoDB database"""
    global db, client
    if client is not None:
        client.close()
        print("MONGODB DISCONNECTED")

def get_db() -> AsyncIOMotorDatabase:
    """Get the database instance"""
    if db is None:
        raise RuntimeError("Database not connected")
    return db
