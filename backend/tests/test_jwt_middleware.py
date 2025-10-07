"""
Test JWT Middleware for Supabase Auth Verification
"""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import os

# Import the middleware function
from src.api.middleware.jwt_middleware import verify_token


def test_verify_token_missing_secret():
    """Test JWT verification when secret is missing"""
    # Temporarily remove the JWT secret
    original_secret = os.environ.get("SUPABASE_JWT_SECRET")
    if original_secret:
        del os.environ["SUPABASE_JWT_SECRET"]

    # Create mock credentials
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="fake-token"
    )

    # Should raise HTTP 500 error
    with pytest.raises(HTTPException) as exc_info:
        verify_token(credentials)

    assert exc_info.value.status_code == 500
    assert "Server configuration error" in str(exc_info.value.detail)

    # Restore the secret
    if original_secret:
        os.environ["SUPABASE_JWT_SECRET"] = original_secret


def test_verify_token_invalid_token():
    """Test JWT verification with invalid token"""
    # Set a fake JWT secret for testing
    original_secret = os.environ.get("SUPABASE_JWT_SECRET")
    os.environ["SUPABASE_JWT_SECRET"] = "test-secret-key"

    # Create mock credentials with invalid token
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="invalid-token"
    )

    # Should raise HTTP 401 error
    with pytest.raises(HTTPException) as exc_info:
        verify_token(credentials)

    assert exc_info.value.status_code == 401
    assert "Invalid or expired token" in str(exc_info.value.detail)

    # Restore the original secret
    if original_secret:
        os.environ["SUPABASE_JWT_SECRET"] = original_secret
    elif "SUPABASE_JWT_SECRET" in os.environ:
        del os.environ["SUPABASE_JWT_SECRET"]
