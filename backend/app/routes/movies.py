from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.movies import Movie
from app.services.movies_service import fetch_all_movies, fetch_movie_by_id, create_movie, delete_movie

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

@router.get("/", response_model=list[Movie])
def get_movies(db: Session = Depends(get_db)):
    """
    Fetch all movies from the movies table.
    """
    movies = fetch_all_movies(db)
    return movies

@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single movie by its ID.
    """
    movie = fetch_movie_by_id(movie_id, db)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    return movie

@router.post("/", status_code=201)
def add_movie(movie: Movie, db: Session = Depends(get_db)):
    """
    Add a new movie to the movies table.
    """
    movie_data = movie.dict()
    create_movie(movie_data, db)
    return {"message": "Movie added successfully"}

@router.delete("/{movie_id}", status_code=204)
def remove_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie by its ID.
    """
    movie = fetch_movie_by_id(movie_id, db)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    delete_movie(movie_id, db)
    return {"message": "Movie deleted successfully"}