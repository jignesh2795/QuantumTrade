"""
Security Middleware for QuantumTrade Platform
"""

import time
from typing import Dict, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging
import hashlib
import hmac

from ...config.security import security_config

logger = logging.getLogger(__name__)

# In-memory storage for rate limiting (in production, use Redis)
rate_limit_storage: Dict[str, Dict[str, int]] = {}


class SecurityMiddleware:
    """Security middleware for handling security-related tasks"""

    def __init__(self):
        self.security_config = security_config

    async def __call__(self, request: Request, call_next):
        """Process incoming requests"""
        try:
            # Add security headers
            response = await call_next(request)

            # Apply security headers
            for header, value in self.security_config.SECURITY_HEADERS.items():
                response.headers[header] = value

            # Set secure cookies if needed
            if self.security_config.SESSION_COOKIE_SECURE:
                response.set_cookie(
                    "session",
                    "",
                    secure=True,
                    httponly=self.security_config.SESSION_COOKIE_HTTPONLY,
                    samesite=self.security_config.SESSION_COOKIE_SAMESITE,
                )

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )

    async def check_rate_limit(self, request: Request) -> Optional[JSONResponse]:
        """Check if request exceeds rate limits"""
        if not self.security_config.RATE_LIMIT_ENABLED:
            return None

        client_ip = request.client.host
        current_time = int(time.time())
        window_start = current_time - self.security_config.RATE_LIMIT_WINDOW

        # Clean old entries
        if client_ip in rate_limit_storage:
            rate_limit_storage[client_ip] = {
                timestamp: count
                for timestamp, count in rate_limit_storage[client_ip].items()
                if int(timestamp) > window_start
            }

        # Count requests in current window
        request_count = sum(
            count for timestamp, count in rate_limit_storage.get(client_ip, {}).items()
        )

        # Check if limit exceeded
        if request_count >= self.security_config.RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429, content={"detail": "Rate limit exceeded"}
            )

        # Update request count
        timestamp = str(current_time)
        if client_ip not in rate_limit_storage:
            rate_limit_storage[client_ip] = {}
        rate_limit_storage[client_ip][timestamp] = (
            rate_limit_storage[client_ip].get(timestamp, 0) + 1
        )

        return None

    def verify_api_key(self, request: Request) -> bool:
        """Verify API key in request headers"""
        if not self.security_config.API_KEY_REQUIRED:
            return True

        api_key = request.headers.get(self.security_config.API_KEY_HEADER)
        if not api_key:
            return False

        # In a real implementation, you would verify the API key against a database
        # For now, we'll just check if it's not empty
        return len(api_key) > 0

    def generate_csrf_token(self, secret_key: str, session_id: str) -> str:
        """Generate CSRF token"""
        timestamp = str(int(time.time()))
        message = f"{session_id}:{timestamp}"
        return hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

    def verify_csrf_token(self, secret_key: str, session_id: str, token: str) -> bool:
        """Verify CSRF token"""
        # In a real implementation, you would verify the token
        # For now, we'll just check if it's not empty
        return len(token) > 0 if self.security_config.CSRF_PROTECTION_ENABLED else True


# Global security middleware instance
security_middleware = SecurityMiddleware()
