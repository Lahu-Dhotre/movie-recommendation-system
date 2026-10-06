from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.movie_ratings import MovieRating, MovieRatingCreate
from app.services.movie_ratings import (
    fetch_all_ratings,
    fetch_ratings_by_user,
    fetch_ratings_by_movie,
    create_rating,
    delete_rating,
)

router = APIRouter(prefix="/api/v1/movie_ratings", tags=["Movie Ratings"])

@router.get("/", response_model=list[MovieRating])
def get_all_ratings(db: Session = Depends(get_db)):
    """
    Fetch all ratings from the movie_ratings table.
    """
    ratings = fetch_all_ratings(db)
    return ratings

@router.get("/user/{user_name}", response_model=list[MovieRating])
def get_ratings_by_user(user_name: str, db: Session = Depends(get_db)):
    """
    Fetch all ratings by a specific user.
    """
    ratings = fetch_ratings_by_user(user_name, db)
    if not ratings:
        raise HTTPException(status_code=404, detail=f"No ratings found for user {user_name}")
    return ratings

@router.get("/movie/{movie_id}", response_model=list[MovieRating])
def get_ratings_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Fetch all ratings for a specific movie.
    """
    ratings = fetch_ratings_by_movie(movie_id, db)
    if not ratings:
        raise HTTPException(status_code=404, detail=f"No ratings found for movie ID {movie_id}")
    return ratings

@router.post("/", status_code=201)
def add_rating(rating: MovieRatingCreate, db: Session = Depends(get_db)):
    """
    Add a new rating to the movie_ratings table.
    """
    rating_data = rating.dict()
    create_rating(rating_data, db)
    return {"message": "Rating added successfully"}

@router.delete("/{rating_id}", status_code=204)
def remove_rating(rating_id: int, db: Session = Depends(get_db)):
    """
    Delete a rating by its ID.
    """
    delete_rating(rating_id, db)
    return {"message": "Rating deleted successfully"}