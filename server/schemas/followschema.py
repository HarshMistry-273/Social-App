from pydantic import BaseModel


class CreateFollow(BaseModel):
    followed_id: str

