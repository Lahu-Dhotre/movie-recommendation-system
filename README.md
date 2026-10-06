# Movie Recommendation System

A full-stack movie recommendation application built with an Angular frontend and a FastAPI backend. The platform combines movie metadata from TMDB with a collaborative filtering recommendation model to suggest movies for a given user.

## Overview

This project is structured as a monorepo with two main parts:

- `frontend/movie-app` — Angular UI for browsing movies and interacting with the recommendation system
- `backend` — FastAPI service for movie data, user/rating APIs, and recommendation logic

The backend loads a trained collaborative filtering model from `backend/app/ml_models/user_cf_model.pkl` and exposes recommendation endpoints based on user ratings.

## Features

- Personalized movie recommendations for a user ID
- TMDB integration for fetching popular movie information
- User, movie, and rating API endpoints
- Angular-based front-end interface
- FastAPI backend with CORS enabled for local development
- SQLAlchemy database access with environment-based configuration

## Tech Stack

- Frontend: Angular 20, TypeScript, Angular Material
- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- ML/Recommender: collaborative filtering model (pickle-based), pandas, NumPy
- External API: TMDB API
- Database: MySQL-compatible database configured through environment variables

## Project Structure

```text
movie-recommendation-system/
├── backend/
│   ├── app/
│   │   ├── ml_models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── import_movies.py
│   │   ├── main.py
│   │   ├── recommender.ipynb
│   │   ├── tmdb_client.py
│   │   └── ...
│   └── requirements.txt
├── frontend/
│   └── movie-app/
│       ├── src/
│       ├── package.json
│       ├── angular.json
│       └── README.md
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Node.js 18+
- npm
- A MySQL-compatible database instance
- A TMDB API key

## Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
# .venv\Scripts\activate    # On Windows
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` folder with the following values:

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=movie_recommendation
TMDB_API_KEY=your_tmdb_api_key
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w300
```

5. Ensure the trained model exists:

```text
backend/app/ml_models/user_cf_model.pkl
```

If this file is missing, the recommendation endpoint will fail during startup.

6. Start the API server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend should be available at:

- http://localhost:8000

## Frontend Setup

1. Navigate to the Angular app:

```bash
cd frontend/movie-app
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run "start frontend"
```

The frontend should be available at:

- http://localhost:4200

## API Overview

The backend exposes movie recommendation and data endpoints through FastAPI. A key endpoint is:

```http
GET /api/v1/recommendations/{user_id}?n_recommendations=5
```

This endpoint fetches the user's rating history, applies the collaborative filtering model, and returns the top recommended movies.

Other areas of the backend include:

- User APIs
- Movie APIs
- Movie rating APIs
- TMDB integration utilities

## Running the Full Application

Open both services in separate terminals:

- Backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- Frontend: `npm run "start frontend"`

Then open the browser at:

- http://localhost:4200

## Notes

- The app is configured for local development and uses CORS for `localhost:4200` and `localhost:8000`.
- Recommended model files and database data must be present for the recommendation engine to function correctly.
- The project includes a Jupyter notebook (`backend/app/recommender.ipynb`) for experimentation and model-related work.

## License

This project does not currently declare a specific license in the repository. If you plan to distribute or reuse it, confirm the license before publishing.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

This README provides a practical starting point for running and understanding the movie recommendation system locally.
