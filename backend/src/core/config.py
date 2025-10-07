import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration settings."""

    # Supabase configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Application settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8000))

    # AI/ML settings
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")

    # Backtesting settings
    BACKTEST_DATA_PATH = os.getenv("BACKTEST_DATA_PATH", "./data")

    # Security settings
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

    # Scalability settings
    # Worker Configuration
    WORKER_COUNT: int = int(os.getenv("WORKER_COUNT", "4"))
    WORKER_TIMEOUT: int = int(os.getenv("WORKER_TIMEOUT", "30"))

    # Queue Configuration (for async tasks)
    QUEUE_MAX_SIZE: int = int(os.getenv("QUEUE_MAX_SIZE", "1000"))
    QUEUE_TIMEOUT: int = int(os.getenv("QUEUE_TIMEOUT", "30"))

    # Caching Configuration
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "10000"))

    # Database Connection Pool
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "30"))

    # API Rate Limiting
    API_RATE_LIMIT: str = os.getenv("API_RATE_LIMIT", "100/minute")

    # Load Balancing
    ENABLE_LOAD_BALANCING: bool = (
        os.getenv("ENABLE_LOAD_BALANCING", "false").lower() == "true"
    )

    # Microservice Configuration
    ENABLE_MICROSERVICES: bool = (
        os.getenv("ENABLE_MICROSERVICES", "false").lower() == "true"
    )

    # Async Processing
    ENABLE_ASYNC_PROCESSING: bool = (
        os.getenv("ENABLE_ASYNC_PROCESSING", "true").lower() == "true"
    )
