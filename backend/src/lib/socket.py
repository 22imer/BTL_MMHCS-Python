"""
Socket.IO configuration for real-time messaging
Uses python-socketio with ASGI compatibility
"""

import socketio
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Create Socket.IO server instance with ASGI support
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['*'],
    ping_timeout=60,
    ping_interval=25,
    engineio_logger=False,
    logger=False
)

# Dictionary to store online users: {user_id: socket_id}
user_socket_map: Dict[str, str] = {}


def get_receiver_socket_id(user_id: str) -> Optional[str]:
    """Get socket ID for a specific user"""
    return user_socket_map.get(str(user_id))


def get_online_users() -> list:
    """Get list of online user IDs"""
    return list(user_socket_map.keys())


async def emit_online_users():
    """Broadcast online users list to all connected clients"""
    await sio.emit("getOnlineUsers", get_online_users(), broadcast=True)


async def emit_new_message(receiver_id: str, message_data: dict):
    """Emit new message to receiver if they're online"""
    receiver_socket_id = get_receiver_socket_id(receiver_id)
    if receiver_socket_id:
        await sio.emit("newMessage", message_data, room=receiver_socket_id)


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    try:
        logger.info(f"Client {sid} connected")
    except Exception as e:
        logger.error(f"Error in connect handler: {e}")


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    try:
        # Find and remove user from online map
        user_id = None
        for uid, socket_id in list(user_socket_map.items()):
            if socket_id == sid:
                user_id = uid
                del user_socket_map[uid]
                break
        
        if user_id:
            logger.info(f"User {user_id} disconnected (socket: {sid})")
            # Broadcast updated online users list
            await emit_online_users()
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")


@sio.event
async def user_connected(sid, data):
    """Handle user connection with user ID (called by client after authentication)"""
    try:
        user_id = data.get("userId")
        if user_id:
            user_socket_map[str(user_id)] = sid
            logger.info(f"User {user_id} is now online (socket: {sid})")
            # Broadcast updated online users list
            await emit_online_users()
    except Exception as e:
        logger.error(f"Error in user_connected: {e}")


