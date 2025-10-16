import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.logger import setup_logger

# Create a logger with DEBUG level to see all messages
logger = setup_logger("test", level="DEBUG")

print("Testing colored output:")
print("======================")

# Test different log levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

print("======================")
print("Test completed")