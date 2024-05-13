import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey,Integer, func
from server.db import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    content = Column(String)
    uid = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default= func.now())
    updated_at = Column(DateTime, onupdate= func.now())
    like_cnt = Column(Integer, default=0)
    comment_cnt = Column(Integer, default=0)