"""
Authentication API Routes for QuantumTrade Platform
Provides endpoints for user authentication and JWT token management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta
import jwt
import logging
import hashlib
import os

from ...utils.security import verify_password, create_access_token, get_password_hash
from ...config.security import security_config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Simulated user database (in production, this would be a real database)
USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash(
            "admin123"
        ),  # In production, never hardcode passwords
        "email": "admin@quantumtrade.com",
        "disabled": False,
    },
    "trader": {
        "username": "trader",
        "hashed_password": get_password_hash("trader123"),
        "email": "trader@quantumtrade.com",
        "disabled": False,
    },
}


def authenticate_user(username: str, password: str):
    """
    Authenticate a user

    Args:
        username: Username
        password: Password

    Returns:
        User dict if authenticated, False otherwise
    """
    user = USERS_DB.get(username)
    if not user:
        return False
    if user.get("disabled", False):
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current authenticated user from JWT token

    Args:
        token: JWT token

    Returns:
        User dict
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = USERS_DB.get(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and get access token

    Args:
        form_data: Form data with username and password

    Returns:
        JWT access token
    """
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(
            minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"username": user["username"], "email": user["email"]},
        }
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register")
async def register_user(username: str, email: str, password: str):
    """
    Register a new user (simplified for demo)

    Args:
        username: Username
        email: Email address
        password: Password

    Returns:
        Registration confirmation
    """
    try:
        # Check if user already exists
        if username in USERS_DB:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Create new user
        hashed_password = get_password_hash(password)
        USERS_DB[username] = {
            "username": username,
            "hashed_password": hashed_password,
            "email": email,
            "disabled": False,
        }

        logger.info(f"New user registered: {username}")

        return {"status": "success", "message": "User registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user information

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    try:
        return {
            "status": "success",
            "user": {
                "username": current_user["username"],
                "email": current_user["email"],
            },
        }
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme)):
    """
    Logout user (invalidate token)

    Args:
        token: JWT token to invalidate

    Returns:
        Logout confirmation
    """
    try:
        # In a real implementation, you would add the token to a blacklist
        # For this demo, we'll just return success
        return {"status": "success", "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh access token

    Args:
        current_user: Current authenticated user

    Returns:
        New JWT access token
    """
    try:
        # Create new access token
        access_token_expires = timedelta(
            minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": current_user["username"]}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/validate")
async def validate_token(token: str = Depends(oauth2_scheme)):
    """
    Validate JWT token

    Args:
        token: JWT token to validate

    Returns:
        Token validation result
    """
    try:
        payload = jwt.decode(
            token, security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = USERS_DB.get(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return {"status": "valid", "username": username, "exp": payload.get("exp")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
