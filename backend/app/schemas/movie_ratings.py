from pydantic import BaseModel
from datetime import datetime

class MovieRating(BaseModel):
    id: int
    user_name: str
    movie_id: int
    rating: int  # Rating is an integer (0-5)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class MovieRatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int  # Rating is an integer (0-5)