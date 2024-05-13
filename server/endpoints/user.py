from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
from server.schemas import userschema, followschema
from server.models import usermodel, followmodel
from sqlalchemy.orm import Session
from server.common import get_db, hash_pswd, verify_password
from server.crud import create, delete
from server.utils import auth, otp
from jose import jwt
from server.config  import Config
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params, Page
from sqlalchemy import select

route = APIRouter(prefix='/User', tags=['User'])


@route.get('/get_all_users', response_model=List[userschema.ViewUsers])
def get_paginated_users(db: Session = Depends(get_db), params: Params = Depends()):
    query = select(usermodel.User).order_by(usermodel.User.id)
    paginated_query = paginate(db, query, params=params)
    return paginated_query.items



@route.post('/CreateUser', status_code=status.HTTP_201_CREATED)
def register(user: userschema.CreateUser, db:Session = Depends(get_db)):

    try:
        existing_user = db.query(usermodel.User).filter(usermodel.User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        if user.password != user.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password do not match")
        
        hash_password = hash_pswd(user.password)

        new_user = usermodel.User(full_name = user.full_name,
                                email = user.email,
                                phno = user.phno,
                                username = user.username,
                                password = hash_password
                                )    
        create(new_user, db)

        return({"Message": "User Created successfully"})
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.post('/GetOTPForVerification', status_code=status.HTTP_201_CREATED)
def generate_otp(email, db:Session = Depends(get_db)):

    try:
        code = otp.generate_otp(email, db)
        otp.send_mail(email, code)
        return {"Message" : "OTP sent successfully"}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.post('/VerifyOTP')
def verify_otp(code, email,db:Session = Depends(get_db)):

    try:
        check = otp.verify_otp(code, email,db)
        if check:
            user = db.query(usermodel.User).filter(usermodel.User.email == email).first()
            user.is_verified = True
            db.commit()
            return {"Message": "Verification Successful"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or OTP expired")

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@route.post('/Login')
def login(username: str, password: str,  db:Session = Depends(get_db)):

    try:
        user = db.query(usermodel.User).filter(usermodel.User.username == username).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verify your email first")
        
        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password didn't match")
        
        token = auth.create_access_token({"id":user.id,"username":user.username})
        rtoken = auth.create_refresh_token({"id":user.id,"username":user.username})
        return {"ACCESS_TOKEN": token, "REFRESH_TOKEN": rtoken}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.get('/Profile')
def view_profile(
    current_user = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        follower_count = (
            db.query(followmodel.Follow)
            .filter(followmodel.Follow.following_id == current_user.id)
            .count()
        )
        followed_count = (
            db.query(followmodel.Follow)
            .filter(followmodel.Follow.follower_id == current_user.id)
            .count()
        )
        
        user_data = userschema.ViewUser(
            full_name=current_user.full_name,
            email=current_user.email,
            phno=current_user.phno,
            username=current_user.username,
            following=followed_count,
            followers=follower_count
        )
        
        return user_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@route.put('/UpdatePassword')
def change_password(password: userschema.UpdatePassword, db:Session = Depends(get_db),current_user = Depends(auth.get_current_user)):

    try:
        if password.new_password != password.confirm_newpassword:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.")
        current_user.password = hash_pswd(password.new_password)
        db.commit()
        return{"Message": "Password changed"}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@route.post('/ForgotPassword')
def forgot_pswd(email,db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        code = otp.generate_otp(email, db)
        otp.send_mail(email, code)
        return {"Message" : "OTP sent successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.post('/VerifyOTPToResetPassword')
def reset_pswd(new_pswd: userschema.ForgetPassword, db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        check = otp.verify_otp(new_pswd.otp_code, current_user.email, db)
        if check:
            current_user.password = hash_pswd(new_pswd.new_password)
            db.commit()
            return {"Message": "Password changed Successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or OTP expired")
        
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@route.post('/Follow')
def follow_user(flw: followschema.CreateFollow, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        ext_follow = db.query(followmodel.Follow).filter(followmodel.Follow.follower_id == current_user.id, followmodel.Follow.following_id == flw.followed_id).first()
        if ext_follow:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already following")
        
        follow = followmodel.Follow(
                    follower_id = current_user.id,
                    following_id = flw.followed_id
            )
        create(follow, db)
        return {"Message": "Following"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @route.get("/")
# def read_user(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

#     try:
#         user = db.query(usermodel.User).filter(usermodel.User.id == current_user.id).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#       
#         follower_count = db.query(followmodel.Follow).filter(followmodel.Follow.following_id == current_user.id).count()
#         followed_count = db.query(followmodel.Follow).filter(followmodel.Follow.follower_id == current_user.id).count()
#
#         user_data = {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "follower_count": follower_count,
#             "following_count": followed_count
#         }
#         return user_data
#
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.delete('/Unfollow')
def unfollow(fid: str, db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        ext_flw = ext_follow = db.query(followmodel.Follow).filter(followmodel.Follow.follower_id == current_user.id, followmodel.Follow.following_id == fid).first()
        if not ext_flw:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Following")
        delete(ext_flw, db)
        return {"Message": "Unfollowed"}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


@route.post('/refresh_token')
def refresh_token(refresh_token: str, current_user = Depends(auth.get_current_user)):
    try: 
        payload = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
        uid = payload.get('id')
        if uid is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        new_access_token = auth.create_access_token({"id":current_user.id,"username":current_user.username})
        return {"token": new_access_token}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# add_pagination(route)