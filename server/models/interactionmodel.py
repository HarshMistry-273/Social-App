import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Session
from server.db import Base


class Like(Base):
    __tablename__ = 'likes'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    pid = Column(String, ForeignKey('posts.id'))
    uid = Column(String, ForeignKey('users.id'))


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    comm = Column(String)
    pid = Column(String, ForeignKey('posts.id'))
    uid = Column(String, ForeignKey('users.id'))
    done_at = Column(DateTime, default=func.now())