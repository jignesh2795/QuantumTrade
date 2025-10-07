"""
Main Server Module for QuantumTrade Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import logging
import time

from .routes import router
from .middleware.security_middleware import security_middleware
from ..config.security import security_config
from ..utils.metrics import metrics_collector
from ..database.connection import get_database_status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="QuantumTrade API",
    description="AI-powered trading platform API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=security_config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add security middleware
@app.middleware("http")
async def security_middleware_handler(request, call_next):
    """Apply security middleware to all requests"""
    # Check rate limiting
    rate_limit_response = await security_middleware.check_rate_limit(request)
    if rate_limit_response:
        return rate_limit_response

    # Apply security middleware
    response = await security_middleware(request, call_next)
    return response


# Add metrics middleware
@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Collect metrics for API requests"""
    start_time = time.time()

    try:
        response = await call_next(request)
        return response
    finally:
        # Record API request metrics
        latency = time.time() - start_time
        metrics_collector.record_api_request(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code if "response" in locals() else 500,
        )
        metrics_collector.record_trade_latency(latency)


# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    db_status = get_database_status()
    return {"message": "QuantumTrade API is running!", "database_status": db_status}


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "uptime": metrics_collector.get_uptime()}


# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest

    return Response(generate_latest(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
