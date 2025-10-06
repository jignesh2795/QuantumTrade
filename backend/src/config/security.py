"""
Security configuration for QuantumTrade
"""
import os
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "default_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_DELTA: int = int(os.getenv("JWT_EXPIRATION_DELTA", "3600"))
    
    # API Security
    API_KEY_HEADER: str = "X-API-Key"
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
    ]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

# Security utilities
def hash_password(password: str) -> str:
    """Hash a password (placeholder implementation)"""
    # In a real implementation, use a proper hashing library like bcrypt
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash (placeholder implementation)"""
    return hash_password(plain_password) == hashed_password

def generate_api_key() -> str:
    """Generate a random API key (placeholder implementation)"""
    import secrets
    return secrets.token_urlsafe(32)

# Input validation utilities
def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", "&", "\"", "'", ";", "--", "/*", "*/"]
    sanitized = input_str
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    return sanitized.strip()

def validate_symbol(symbol: str) -> bool:
    """Validate that a symbol is safe"""
    if not symbol or len(symbol) > 10:
        return False
    # Only allow alphanumeric characters and common separators
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
    return all(c in allowed_chars for c in symbol.upper())