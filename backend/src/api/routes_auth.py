"""
Simplified Auth Routes for QuantumTrade Platform
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..auth.supabase_auth import authenticate_user, register_user, verify_token

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(request: LoginRequest):
    """
    Login user

    Args:
        request: Login request with email and password

    Returns:
        Authentication result
    """
    try:
        response = authenticate_user(request.email, request.password)
        return {
            "status": "success",
            "message": "Login successful",
            "user": response.user,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {e}")


@router.post("/register")
async def register(request: RegisterRequest):
    """
    Register new user

    Args:
        request: Registration request with email and password

    Returns:
        Registration result
    """
    try:
        response = register_user(request.email, request.password)
        return {
            "status": "success",
            "message": "Registration successful",
            "user": response.user,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {e}")


@router.get("/profile")
async def get_profile(user=Depends(verify_token)):
    """
    Get user profile (requires authentication)

    Args:
        user: Authenticated user (from token)

    Returns:
        User profile information
    """
    return {
        "status": "success",
        "user": {
            "id": user.get("sub"),
            "email": user.get("email"),
            "role": user.get("role", "user"),
        },
    }


@router.get("/verify")
async def verify_auth():
    """
    Verify authentication status

    Returns:
        Authentication status
    """
    return {"status": "Authentication system is active"}
