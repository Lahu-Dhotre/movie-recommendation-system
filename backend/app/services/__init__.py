from sqlalchemy.orm import Session
from sqlalchemy import text

def fetch_all_users(db: Session):
    """
    Fetch all users from the database.
    """
    return db.execute(text("SELECT * FROM users")).fetchall()