from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from src.controllers.auth_controller import (
    signup,
    login,
    logout,
    update_profile,
    check_auth
)
from src.middleware.auth_middleware import protect_route
from src.models.User import UserCreate, UserLogin, UserUpdate

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup")
async def signup_route(request: Request, response: Response):
    """User signup endpoint"""
    try:
        data = await request.json()
        email = data.get("email")
        fullName = data.get("fullName")
        password = data.get("password")
        
        result, status_code, token = await signup(email, fullName, password)
        
        if status_code == 201:
            # Set JWT cookie
            response.set_cookie(
                key="jwt",
                value=token,
                max_age=7 * 24 * 60 * 60,
                httponly=True,
                samesite="strict",
                secure=False  # Set to True in production
            )
        
        response.status_code = status_code
        return result
        
    except Exception as e:
        print(f"Error in signup route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login")
async def login_route(request: Request, response: Response):
    """User login endpoint"""
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        result, status_code, token = await login(email, password)
        
        if status_code == 200:
            # Set JWT cookie
            response.set_cookie(
                key="jwt",
                value=token,
                max_age=7 * 24 * 60 * 60,
                httponly=True,
                samesite="strict",
                secure=False  # Set to True in production
            )
        
        response.status_code = status_code
        return result
        
    except Exception as e:
        print(f"Error in login route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout")
async def logout_route(response: Response):
    """User logout endpoint"""
    try:
        result, status_code = await logout()
        
        # Clear JWT cookie
        response.delete_cookie(key="jwt")
        
        response.status_code = status_code
        return result
        
    except Exception as e:
        print(f"Error in logout route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/update-profile")
async def update_profile_route(request: Request, response: Response, user=Depends(protect_route)):
    """Update user profile endpoint"""
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )
        
        data = await request.json()
        fullName = data.get("fullName")
        profilePic = data.get("profilePic")
        
        user_id = str(user.get("_id"))
        result, status_code = await update_profile(user_id, fullName, profilePic)
        
        response.status_code = status_code
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_profile route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/check")
async def check_auth_route(user=Depends(protect_route)):
    """Check if user is authenticated"""
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in check_auth route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
