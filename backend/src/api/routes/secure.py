"""
Secure API Routes for QuantumTrade Platform
Protected routes that require JWT token verification
"""

from fastapi import APIRouter, Depends
import logging

from ..middleware.jwt_middleware import verify_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/secure", tags=["secure"])


@router.get("/profile")
def get_user_profile(user=Depends(verify_token)):
    """
    Get user profile information (requires authentication)

    Args:
        user: Decoded JWT token payload

    Returns:
        User profile information
    """
    try:
        # Extract user information from token
        user_id = user.get("sub")
        email = user.get("email")

        return {
            "status": "success",
            "message": "Authenticated user profile",
            "user": {"id": user_id, "email": email, "role": user.get("role", "user")},
        }
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return {"status": "error", "message": "Failed to fetch user profile"}


@router.get("/data")
def get_secure_data(user=Depends(verify_token)):
    """
    Get secure data (requires authentication)

    Args:
        user: Decoded JWT token payload

    Returns:
        Secure data
    """
    try:
        return {
            "status": "success",
            "message": "You are authenticated",
            "user": user,
            "data": {
                "secret_info": "This is protected data only accessible to authenticated users",
                "timestamp": "2025-10-07T10:00:00Z",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching secure data: {e}")
        return {"status": "error", "message": "Failed to fetch secure data"}
