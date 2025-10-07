# FastAPI Uvicorn runner
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.server import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)
