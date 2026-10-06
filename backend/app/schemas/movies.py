from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    poster_url: Optional[str]  # Optional field for the movie poster URL
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True