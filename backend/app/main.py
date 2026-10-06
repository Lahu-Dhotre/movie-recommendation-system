# app/main.py
from typing import List
from app import schemas
from app.tmdb_client import fetch_popular_movies, transform_tmdb_movie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
from fastapi import FastAPI, HTTPException
import pickle   
import pandas as pd
import numpy as np
from app.schemas.users import UserSchema
from app.services.users_service import fetch_all_users
from app.schemas import Movie
from app.schemas.users import UserSchema
from app.routes import users, movies, movie_ratings
from app.services.movies_service import fetch_movie_by_id  # Import the users, movies, and movie_ratings routers
from .database import get_db  # adjust import based on your folder structure
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Log file name
    filemode="w",        # Overwrite the file each time the server starts
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Movie Recommender Backend (TMDB Proxy)")

app.include_router(users.router)  # Include the users router
app.include_router(movies.router)  # Include the movies router
app.include_router(movie_ratings.router)  # Include the movie_ratings router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:4200"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model when the application starts
@app.on_event("startup")
def load_user_cf_model():
    global user_cf_model
    try:
        with open("app/ml_models/user_cf_model.pkl", "rb") as f:
            user_cf_model = pickle.load(f)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Model file not found. Ensure 'user_cf_model.pkl' exists in 'app/ml_models/' directory.")
        user_cf_model = None
        

from app.services.oracle_service import fetch_user_data
from sqlalchemy.orm import Session
from fastapi import Depends


@app.get("/api/v1/recommendations/{user_id}")
def get_recommendations(user_id: int, n_recommendations: int = 5, db: Session = Depends(get_db)):
    """
    Get movie recommendations for a user based on the collaborative filtering model.
    """
    if user_cf_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please check the server logs.")

    # Fetch user data from Oracle
    user_data = fetch_user_data(user_id, db)
    logging.info(f"User data from database: {user_data}")  # Log user data

    if not user_data:
        raise HTTPException(status_code=404, detail=f"No data found for user ID {user_id}.")

    # Convert user data to a DataFrame (if needed)
    user_ratings_df = pd.DataFrame(user_data, columns=["movie_id", "rating"])

    # Use the collaborative filtering model for predictions
    train_matrix = user_cf_model["train_matrix"]
    user_similarity = user_cf_model["user_similarity"]

    # Check if the user_id exists in the matrix
    user_idx = user_id - 1  # Adjust for zero-based indexing
    logging.info(f"User index in train_matrix: {user_idx}")  # Log user index

    if user_idx not in train_matrix.index:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found in the dataset.")

    # Generate recommendations
    sim_scores = user_similarity[user_idx]
    weighted_ratings = np.dot(sim_scores, train_matrix)
    sum_sim = np.array([np.abs(sim_scores).sum()] * train_matrix.shape[1])
    predicted_ratings = weighted_ratings / np.where(sum_sim == 0, 1, sum_sim)

    logging.info(f"Predicted ratings before exclusion: {predicted_ratings}")  # Log predicted ratings

    # Exclude already rated movies
    already_rated = train_matrix.iloc[user_idx].to_numpy().nonzero()[0]
    predicted_ratings[already_rated] = -np.inf

    logging.info(f"Predicted ratings after exclusion: {predicted_ratings}")  # Log predicted ratings after exclusion

    # Get top N recommendations
    recommended_movie_indices = np.argsort(predicted_ratings)[::-1][:n_recommendations]
    recommended_movie_ids = train_matrix.columns[recommended_movie_indices].tolist()

    logging.info(f"Recommended movie IDs: {recommended_movie_ids}")  # Log recommendations
    
        # Fetch movie details for each recommended movie ID
    recommended_movies = []
    for movie_id in recommended_movie_ids:
        movie = fetch_movie_by_id(int(movie_id), db)
        if movie:
            recommended_movies.append(dict(movie._mapping))

    return {"user_id": user_id, "recommendations": recommended_movies}

from sqlalchemy import text

def fetch_user_data(user_id: int, db: Session):
    """
    Fetch user data from the Oracle database using SQLAlchemy.
    """
    query = text("""
    SELECT movie_id, rating
    FROM movie_ratings
    WHERE user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user_id}).fetchall()
    return result  # Example: [(1, 4.5), (2, 3.0), ...]