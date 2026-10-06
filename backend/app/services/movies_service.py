from sqlalchemy.orm import Session
from sqlalchemy import text

def fetch_all_movies(db: Session):
    """
    Fetch all movies from the movies table.
    """
    query = text("SELECT * FROM movies")
    return db.execute(query).fetchall()

def fetch_movie_by_id(movie_id: int, db: Session):
    """
    Fetch a single movie by its ID.
    """
    query = text("SELECT * FROM movies WHERE id = :movie_id")
    return db.execute(query, {"movie_id": movie_id}).fetchone()

def create_movie(movie_data: dict, db: Session):
    """
    Insert a new movie into the movies table.
    """
    query = text("""
        INSERT INTO movies (title, overview, poster_url)
        VALUES (:title, :overview, :poster_url)
    """)
    db.execute(query, movie_data)
    db.commit()

def delete_movie(movie_id: int, db: Session):
    """
    Delete a movie by its ID.
    """
    query = text("DELETE FROM movies WHERE id = :movie_id")
    db.execute(query, {"movie_id": movie_id})
    db.commit()