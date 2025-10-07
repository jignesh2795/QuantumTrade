"""
Security Configuration for QuantumTrade Platform
"""

import os
from typing import List


class SecurityConfig:
    """Security configuration settings"""

    # Secret key for JWT tokens (should be set in environment variables in production)
    SECRET_KEY = os.getenv("SECRET_KEY", "quantumtrade_secret_key_for_jwt_tokens")

    # Algorithm for JWT tokens
    ALGORITHM = "HS256"

    # Token expiration time (in minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Frontend development server
        "http://localhost:3000",  # Alternative frontend port
        "http://localhost",  # Local development
        "https://yourdomain.com",  # Production domain
    ]

    # Allowed hosts
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "yourdomain.com",
    ]

    # Security headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    }

    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 3600))  # 1 hour

    # Password security
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGITS = True
    PASSWORD_REQUIRE_SPECIAL_CHARS = True

    # API security
    API_KEY_HEADER = "X-API-Key"
    API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"

    # SSL/TLS settings
    SSL_ENABLED = os.getenv("SSL_ENABLED", "false").lower() == "true"

    # Session security
    SESSION_COOKIE_SECURE = SSL_ENABLED
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # CSRF protection
    CSRF_PROTECTION_ENABLED = True
    CSRF_COOKIE_SECURE = SSL_ENABLED
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = "Lax"


# Global security config instance
security_config = SecurityConfig()
