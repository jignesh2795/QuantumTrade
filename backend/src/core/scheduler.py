"""
Scheduler module for QuantumTrade backend.
Handles background tasks such as data fetching and synchronization.
"""

import asyncio
from datetime import datetime
from typing import Callable, Dict
from .event_bus import event_bus


class Scheduler:
    """Background task scheduler."""

    def __init__(self):
        self._tasks: Dict[str, asyncio.Task] = {}
        self._intervals: Dict[str, float] = {}

    async def schedule_task(self, name: str, task: Callable, interval: float):
        """Schedule a recurring task."""

        async def run_task():
            while True:
                try:
                    if asyncio.iscoroutinefunction(task):
                        await task()
                    else:
                        task()
                except Exception as e:
                    print(f"Error in scheduled task {name}: {e}")
                await asyncio.sleep(interval)

        # Cancel existing task if it exists
        if name in self._tasks:
            self._tasks[name].cancel()

        # Schedule new task
        self._tasks[name] = asyncio.create_task(run_task())
        self._intervals[name] = interval

    def cancel_task(self, name: str):
        """Cancel a scheduled task."""
        if name in self._tasks:
            self._tasks[name].cancel()
            del self._tasks[name]
            del self._intervals[name]

    def get_scheduled_tasks(self):
        """Get list of scheduled tasks."""
        return list(self._tasks.keys())


# Global scheduler instance
scheduler = Scheduler()
