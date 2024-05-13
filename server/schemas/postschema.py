from pydantic import BaseModel
from typing import List

from server.schemas.interactionschema import ViewComment

class CreatePost(BaseModel):
    title: str
    content: str

class Post(CreatePost):
    username: str
    like_cnt: int
    comment_cnt: int
    comments: List[ViewComment]


class ViewPosts(BaseModel):
    posts: List[Post]

class UpdatePost(CreatePost):
    pid: str

class DeletePost(BaseModel):
    pid: str


    