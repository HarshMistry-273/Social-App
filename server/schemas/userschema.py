import uuid
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    full_name: str
    email: EmailStr
    phno: str
    username: str
    password: str
    confirm_password: str


class ViewUser(BaseModel):
    full_name: str
    email: EmailStr
    phno: str
    username: str
    followers: int
    following: int

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_newpassword: str

class ForgetPassword(BaseModel):
    otp_code: str
    new_password: str
    confirm_newpassword: str


class ViewUsers(BaseModel):
    full_name: str
    email: str
    is_verified: bool
