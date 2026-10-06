from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    user_id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    img_url: str

    class Config:
        orm_mode = True