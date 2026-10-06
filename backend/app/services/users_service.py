# filepath: c:\Users\mukil\movie_recommendation_system\movie_recommendation_system\backend\app\users_service.py

from sqlalchemy.orm import Session
from sqlalchemy import text

def fetch_all_users(db: Session):
    """
    Fetch all users from the database.
    """
    return db.execute(text("SELECT * FROM users")).fetchall()