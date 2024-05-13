from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from server.common import get_db
from datetime import datetime, timedelta
from server.models import usermodel
from server.config import Config
from jose import jwt,JWTError

OAuth2Scheme = OAuth2PasswordBearer(tokenUrl='/User/Login')

def create_access_token(data: dict,):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY_TIME)
    to_encode.update({'exp': expire,'type': 'access'})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, Config.ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire =datetime.now() + timedelta(days=Config.REFRESH_TOKEN_EXPIRY_TIME)
    to_encode.update({"exp": expire, 'type': 'refresh'})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, Config.ALGORITHM)

    return encoded_jwt



def get_current_user(token: str = Depends(OAuth2Scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        
        uid = payload.get('id')
        if uid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
        
        current_user = db.query(usermodel.User).filter(usermodel.User.id == uid).first()
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return current_user
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
