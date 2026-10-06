from sqlalchemy.orm import Session
from app.database import get_db

def fetch_user_data(user_id: int, db: Session):
    """
    Fetch user data from the Oracle database using SQLAlchemy.
    """
    query = """
    SELECT movie_id, rating
    FROM user_ratings
    WHERE user_id = :user_id
    """
    result = db.execute(query, {"user_id": user_id}).fetchall()
    return result  # Example: [(1, 4.5), (2, 3.0), ...]