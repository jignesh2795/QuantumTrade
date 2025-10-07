"""
Webhooks handler for QuantumTrade Platform
Handles incoming webhooks from Supabase for event-driven updates
"""

from fastapi import APIRouter, Request, HTTPException, Depends
import os
import json
import logging
import hashlib
import hmac

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])

# Environment variables
WEBHOOK_SECRET = os.getenv("SUPABASE_WEBHOOK_SECRET")

def verify_webhook_signature(request: Request, body: bytes) -> bool:
    """
    Verify the webhook signature from Supabase
    
    Args:
        request: FastAPI request object
        body: Raw request body
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not WEBHOOK_SECRET:
        logger.warning("SUPABASE_WEBHOOK_SECRET not configured")
        return False
        
    # Get signature from headers
    signature = request.headers.get("x-supabase-signature")
    if not signature:
        return False
        
    # Verify signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@router.post("/")
async def handle_webhook(request: Request):
    """
    Handle incoming webhook from Supabase
    
    Args:
        request: FastAPI request object
        
    Returns:
        Webhook response
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Verify webhook signature
        if not verify_webhook_signature(request, body):
            raise HTTPException(status_code=403, detail="Unauthorized webhook source")
            
        # Parse JSON data
        data = await request.json()
        
        # Log received webhook
        logger.info(f"📨 Received Supabase Webhook: {data}")
        
        # Process webhook event
        event_type = data.get("type")
        table = data.get("table")
        record = data.get("record")
        
        if event_type and table and record:
            logger.info(f"Processing {event_type} event for table {table}")
            # Here you would implement specific logic based on the event type
            # For example:
            # - Insert/Update/Delete in local database for INSERT/UPDATE/DELETE events
            # - Trigger specific actions based on the table and record data
            
        return {"status": "received", "processed": True}
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def webhook_health():
    """
    Health check endpoint for webhook service
    
    Returns:
        Health status
    """
    return {"status": "healthy", "service": "webhook_handler"}