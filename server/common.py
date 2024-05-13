from server.db import SessionLocal
import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_pswd(password:str):
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)