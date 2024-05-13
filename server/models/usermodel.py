from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
import uuid
from server.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String, unique=True)
    phno = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, onupdate = func.now())
    is_verified = Column(Boolean, default = False)
