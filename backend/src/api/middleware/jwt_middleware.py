"""
JWT Middleware for Supabase Auth Verification
Verifies JWT tokens issued by Supabase for protected routes
"""

import os
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
import logging
from jose import jwt, JWTError

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Get Supabase JWT secret from environment
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not JWT_SECRET:
    logger.warning("SUPABASE_JWT_SECRET not set in environment variables")


def verify_token(credentials=Depends(security)):
    """
    Verify JWT token issued by Supabase

    Args:
        credentials: HTTP Authorization header with Bearer token

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not JWT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: JWT secret not available",
        )

    token = credentials.credentials
    try:
        # Decode JWT token using HS256 algorithm
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )


# Example of how to use this middleware in routes:
#
# from fastapi import APIRouter, Depends
# from src.api.middleware.jwt_middleware import verify_token
#
# router = APIRouter()
#
# @router.get("/secure-data")
# def get_secure_data(user=Depends(verify_token)):
#     return {"message": "You are authenticated", "user": user}
