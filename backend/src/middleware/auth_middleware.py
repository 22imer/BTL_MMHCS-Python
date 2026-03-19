from fastapi import Request, HTTPException, status, Depends
from src.lib.utils import verify_token
from src.lib.db import get_db
from bson import ObjectId


async def protect_route(request: Request):
    """Middleware to protect routes - verify JWT token"""
    try:
        # Get token from cookies
        token = request.cookies.get("jwt")
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - No token provided"
            )
        
        # Verify token
        decoded = verify_token(token)
        
        if not decoded:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - Invalid token"
            )
        
        # Get user from database
        db = get_db()
        user_id = decoded.get("userId")
        
        # Validate ObjectId format
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format"
            )
        
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Remove password from user object and convert _id to string
        user.pop("password", None)
        user["_id"] = str(user.get("_id"))
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in protectRoute middleware: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

