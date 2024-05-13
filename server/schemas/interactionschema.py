from pydantic import BaseModel


class CreateLike(BaseModel):
    pid: str

class CreateComment(BaseModel):
    pid:str
    comm: str

class ViewComment(BaseModel):
    username : str
    comment: str

class UpdateComment(BaseModel):
    cid: str
    comm: str


