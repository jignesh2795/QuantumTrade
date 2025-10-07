"""
Security Utilities for QuantumTrade Platform
Provides password hashing, token generation, and security validation functions
"""

import hashlib
import secrets
import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import os

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY", "quantumtrade-secret-key-for-jwt-tokens-change-in-production"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if passwords match, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        return ""


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time

    Returns:
        JWT access token
    """
    try:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        return ""


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT access token

    Args:
        token: JWT token to verify

    Returns:
        Decoded token data if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.PyJWTError as e:
        logger.error(f"Token verification error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {e}")
        return None


def generate_api_key() -> str:
    """
    Generate a secure API key

    Returns:
        Secure API key
    """
    try:
        return secrets.token_urlsafe(32)
    except Exception as e:
        logger.error(f"Error generating API key: {e}")
        return ""


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for secure storage

    Args:
        api_key: API key to hash

    Returns:
        Hashed API key
    """
    try:
        return hashlib.sha256(api_key.encode()).hexdigest()
    except Exception as e:
        logger.error(f"Error hashing API key: {e}")
        return ""


def verify_api_key(provided_key: str, stored_hash: str) -> bool:
    """
    Verify an API key against its stored hash

    Args:
        provided_key: API key provided by user
        stored_hash: Hashed API key from storage

    Returns:
        True if API key is valid, False otherwise
    """
    try:
        provided_hash = hash_api_key(provided_key)
        return secrets.compare_digest(provided_hash, stored_hash)
    except Exception as e:
        logger.error(f"Error verifying API key: {e}")
        return False


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token

    Args:
        length: Length of the token

    Returns:
        Secure random token
    """
    try:
        return secrets.token_urlsafe(length)
    except Exception as e:
        logger.error(f"Error generating secure token: {e}")
        return ""


def validate_input(data: str, max_length: int = 1000) -> bool:
    """
    Validate input data for security

    Args:
        data: Input data to validate
        max_length: Maximum allowed length

    Returns:
        True if input is valid, False otherwise
    """
    try:
        # Check if data is provided
        if not data:
            return False

        # Check length
        if len(data) > max_length:
            return False

        # Check for potentially dangerous characters
        dangerous_chars = ["<", ">", "&", '"', "'", ";", "--", "/*", "*/"]
        for char in dangerous_chars:
            if char in data:
                return False

        return True
    except Exception as e:
        logger.error(f"Error validating input: {e}")
        return False


def sanitize_input(data: str) -> str:
    """
    Sanitize input data to prevent XSS and other attacks

    Args:
        data: Input data to sanitize

    Returns:
        Sanitized input data
    """
    try:
        if not data:
            return ""

        # Remove or escape dangerous characters
        sanitization_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
            '"': "&quot;",
            "'": "&#x27;",
        }

        sanitized = data
        for char, replacement in sanitization_map.items():
            sanitized = sanitized.replace(char, replacement)

        return sanitized
    except Exception as e:
        logger.error(f"Error sanitizing input: {e}")
        return ""


def rate_limit_key(identifier: str) -> str:
    """
    Generate a key for rate limiting based on identifier

    Args:
        identifier: Unique identifier (e.g., IP address, user ID)

    Returns:
        Rate limit key
    """
    try:
        # Add a salt to prevent key prediction
        salt = hashlib.sha256(SECRET_KEY.encode()).hexdigest()[:8]
        return f"rate_limit:{salt}:{identifier}"
    except Exception as e:
        logger.error(f"Error generating rate limit key: {e}")
        return f"rate_limit:{identifier}"


def is_safe_redirect_url(url: str, allowed_domains: list) -> bool:
    """
    Check if a redirect URL is safe

    Args:
        url: URL to check
        allowed_domains: List of allowed domains

    Returns:
        True if URL is safe, False otherwise
    """
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)

        # Check if URL is relative (no scheme or netloc)
        if not parsed.scheme and not parsed.netloc:
            return True

        # Check if domain is in allowed list
        for domain in allowed_domains:
            if parsed.netloc.endswith(domain):
                return True

        return False
    except Exception as e:
        logger.error(f"Error checking redirect URL safety: {e}")
        return False
