from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserSchema  # Import schema
from app.services.users_service import fetch_all_users  # Import business logic

# Create a router for users
router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    """
    Fetch all users from the users table.
    """
    return fetch_all_users(db)