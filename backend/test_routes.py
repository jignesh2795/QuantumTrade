import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test importing the routes
try:
    from api.routes import router
    print("Routes imported successfully")
    print(f"Router: {router}")
except Exception as e:
    print(f"Error importing routes: {e}")