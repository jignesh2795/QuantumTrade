from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from asyncio import Queue, create_task, gather
import asyncio
import os
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class Event:
    """Base event class"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None
    bot_id: Optional[int] = None
    
    def __str__(self):
        return f"Event({self.type}, bot={self.bot_id}, source={self.source})"


class EventBus:
    """
    Central event bus for communication between components
    Supports pub/sub pattern with async handlers
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_queue: Queue = Queue(maxsize=1000)
        self._running = False
        self._worker_task = None
        logger.info("EventBus initialized")
    
    async def start(self):
        """Start the event bus worker"""
        if self._running:
            logger.warning("EventBus already running")
            return
        
        self._running = True
        self._worker_task = create_task(self._process_events())
        if os.name == 'nt':  # Windows
            logger.info("EventBus started")
        else:
            logger.success("EventBus started")
    
    async def stop(self):
        """Stop the event bus worker"""
        self._running = False
        
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        
        logger.info("EventBus stopped")
    
    def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe to an event type
        
        Args:
            event_type: Event type to subscribe to (e.g., "order.filled")
            handler: Async function to handle the event
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed to {event_type}: {handler.__name__}")
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe from an event type"""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
                logger.debug(f"Unsubscribed from {event_type}: {handler.__name__}")
            except ValueError:
                pass
    
    async def publish(self, event: Event):
        """
        Publish an event to the bus
        
        Args:
            event: Event to publish
        """
        try:
            await self._event_queue.put(event)
            logger.debug(f"Published: {event}")
        except asyncio.QueueFull:
            logger.error(f"Event queue full! Dropping event: {event}")
    
    async def emit(self, event_type: str, data: Dict[str, Any], **kwargs):
        """
        Convenience method to create and publish an event
        
        Args:
            event_type: Type of event
            data: Event data
            **kwargs: Additional event attributes (source, bot_id, etc.)
        """
        event = Event(type=event_type, data=data, **kwargs)
        await self.publish(event)
    
    async def _process_events(self):
        """Worker task to process events from queue"""
        logger.info("Event processing worker started")
        
        while self._running:
            try:
                # Wait for event with timeout
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0
                )
                
                await self._dispatch_event(event)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
        
        logger.info("Event processing worker stopped")
    
    async def _dispatch_event(self, event: Event):
        """Dispatch event to all subscribers"""
        if event.type not in self._subscribers:
            return
        
        handlers = self._subscribers[event.type]
        if not handlers:
            return
        
        # Run all handlers concurrently
        tasks = []
        for handler in handlers:
            try:
                task = create_task(handler(event))
                tasks.append(task)
            except Exception as e:
                logger.error(f"Error creating handler task: {e}")
        
        if tasks:
            # Wait for all handlers with error handling
            results = await gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    handler_name = handlers[i].__name__
                    logger.error(
                        f"Handler {handler_name} failed for {event.type}: {result}"
                    )
    
    def get_subscribers_count(self, event_type: Optional[str] = None) -> int:
        """Get number of subscribers for an event type or total"""
        if event_type:
            return len(self._subscribers.get(event_type, []))
        return sum(len(handlers) for handlers in self._subscribers.values())
    
    def get_event_types(self) -> List[str]:
        """Get all registered event types"""
        return list(self._subscribers.keys())


# Global event bus instance
event_bus = EventBus()


# Event type constants for convenience
class EventTypes:
    """Standard event types used throughout the system"""
    
    # Bot lifecycle
    BOT_STARTED = "bot.started"
    BOT_STOPPED = "bot.stopped"
    BOT_PAUSED = "bot.paused"
    BOT_ERROR = "bot.error"
    
    # Order events
    ORDER_CREATED = "order.created"
    ORDER_FILLED = "order.filled"
    ORDER_CANCELLED = "order.cancelled"
    ORDER_FAILED = "order.failed"
    
    # Position events
    POSITION_OPENED = "position.opened"
    POSITION_CLOSED = "position.closed"
    POSITION_UPDATED = "position.updated"
    
    # Market events
    PRICE_UPDATE = "market.price_update"
    CANDLE_CLOSED = "market.candle_closed"
    
    # Strategy events
    SIGNAL_GENERATED = "strategy.signal"
    STRATEGY_ERROR = "strategy.error"
    
    # Agent events
    AGENT_DECISION = "agent.decision"
    AGENT_ALERT = "agent.alert"
    
    # System events
    SYSTEM_ERROR = "system.error"
    SYSTEM_WARNING = "system.warning"


__all__ = ["Event", "EventBus", "event_bus", "EventTypes"]