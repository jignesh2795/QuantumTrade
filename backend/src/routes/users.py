"""
User routes for QuantumTrade backend.
API endpoints for user/auth functionality.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..models.user import User
from ..core.database import get_db
from ..core.utils import format_response

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register_user(user: UserCreate, db=Depends(get_db)):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user (in a real app, you would hash the password)
        new_user = User(
            email=user.email,
            hashed_password=user.password,  # In reality, hash this!
            full_name=user.full_name,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return format_response(
            {
                "id": new_user.id,
                "email": new_user.email,
                "full_name": new_user.full_name,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login_user(user: UserLogin, db=Depends(get_db)):
    """Login user."""
    try:
        # Find user
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check password (in a real app, you would hash and compare)
        if db_user.hashed_password != user.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return format_response(
            {"id": db_user.id, "email": db_user.email, "message": "Login successful"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me")
async def get_current_user(db=Depends(get_db)):
    """Get current user information."""
    # This is a mock implementation - in reality, you would get the current user from auth
    return format_response(
        {"message": "Current user information would be returned here"}
    )
