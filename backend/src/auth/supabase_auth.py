"""
Supabase Auth for QuantumTrade Platform
Supabase Auth client + JWT verification
"""

from supabase import create_client, Client
import os
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Security scheme
security = HTTPBearer()


def get_supabase_client() -> Client:
    """
    Get Supabase client instance

    Returns:
        Supabase client instance
    """
    return supabase


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token from Supabase

    Args:
        credentials: HTTP Authorization header credentials

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not SUPABASE_JWT_SECRET:
        logger.error("SUPABASE_JWT_SECRET not configured")
        raise HTTPException(status_code=500, detail="Server configuration error")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def authenticate_user(email: str, password: str):
    """
    Authenticate user with Supabase Auth

    Args:
        email: User email
        password: User password

    Returns:
        Authentication response

    Raises:
        HTTPException: If authentication fails
    """
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        return response
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


def register_user(email: str, password: str):
    """
    Register new user with Supabase Auth

    Args:
        email: User email
        password: User password

    Returns:
        Registration response

    Raises:
        HTTPException: If registration fails
    """
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return response
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=400, detail="Registration failed")


def logout_user(token: str):
    """
    Logout user from Supabase Auth

    Args:
        token: User session token

    Returns:
        Logout response

    Raises:
        HTTPException: If logout fails
    """
    try:
        response = supabase.auth.sign_out()
        return response
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")
