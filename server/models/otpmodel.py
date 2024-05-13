import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Session
from server.db import Base

class OTP(Base):
    __tablename__ = 'otp'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    code = Column(String)
    created_at = Column(DateTime, default=func.now())
    email = Column(String)
