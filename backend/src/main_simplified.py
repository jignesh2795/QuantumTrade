"""
Simplified Main Server Module for QuantumTrade Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes
from api.routes import router as trading_router
from api.routes.auth import router as auth_router
from sync.webhooks import router as webhook_router

app.include_router(trading_router, prefix="/api/trade")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(webhook_router, prefix="/webhook")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "QuantumTrade Backend running successfully!"}


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
