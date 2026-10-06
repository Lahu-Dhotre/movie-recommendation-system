# app/tmdb_client.py
from typing import List, Dict, Any
import httpx
from .config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

# Basic list of TMDB movie genres to map ids -> names
# (short list for demo; you can expand if you want)
GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    878: "Science Fiction",
    53: "Thriller",
    27: "Horror",
    10749: "Romance",
}


async def fetch_popular_movies(page: int = 1) -> List[Dict[str, Any]]:
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "page": page,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])


def transform_tmdb_movie(tmdb_movie: Dict[str, Any]) -> Dict[str, Any]:
    # Extract fields from TMDB format and map to our Movie schema
    poster_path = tmdb_movie.get("poster_path")
    poster_url = (
        f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
    )

    release_date = tmdb_movie.get("release_date")
    year = int(release_date[:4]) if release_date else None

    genre_ids = tmdb_movie.get("genre_ids", [])
    genres = [GENRE_MAP.get(gid, str(gid)) for gid in genre_ids]

    return {
        "id": tmdb_movie["id"],
        "title": tmdb_movie.get("title") or tmdb_movie.get("name", ""),
        "year": year,
        "genres": genres,
        "poster_url": poster_url,
        "overview": tmdb_movie.get("overview", ""),
        "global_rating": tmdb_movie.get("vote_average", 0.0),
    }
