from sqlalchemy.orm import Session
from sqlalchemy import text

def fetch_all_ratings(db: Session):
    """
    Fetch all ratings from the movie_ratings table.
    """
    query = text("SELECT * FROM movie_ratings")
    return db.execute(query).fetchall()

def fetch_ratings_by_user(user_name: str, db: Session):
    """
    Fetch all ratings by a specific user.
    """
    query = text("SELECT * FROM movie_ratings WHERE user_name = :user_name")
    return db.execute(query, {"user_name": user_name}).fetchall()

def fetch_ratings_by_movie(movie_id: int, db: Session):
    """
    Fetch all ratings for a specific movie.
    """
    query = text("SELECT * FROM movie_ratings WHERE movie_id = :movie_id")
    return db.execute(query, {"movie_id": movie_id}).fetchall()

def create_rating(rating_data: dict, db: Session):
    """
    Insert a new rating into the movie_ratings table.
    """
    query = text("""
        INSERT INTO movie_ratings (user_id, movie_id, rating)
        VALUES (:user_id, :movie_id, :rating)
    """)
    db.execute(query, rating_data)
    db.commit()

def delete_rating(rating_id: int, db: Session):
    """
    Delete a rating by its ID.
    """
    query = text("DELETE FROM movie_ratings WHERE id = :rating_id")
    db.execute(query, {"rating_id": rating_id})
    db.commit()