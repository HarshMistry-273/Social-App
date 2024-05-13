import uuid
from server.db import Base
from sqlalchemy import Column, String, ForeignKey

class Follow(Base):
    __tablename__ = 'follows'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    follower_id = Column(String, ForeignKey('users.id'))
    following_id = Column(String, ForeignKey('users.id'))