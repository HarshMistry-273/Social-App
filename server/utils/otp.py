import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from server.config import Config
from server.crud import create, delete
from server.models import otpmodel, usermodel
from datetime import datetime, timedelta


def generate_otp(email,db):
    otp_records = db.query(otpmodel.OTP).filter(otpmodel.OTP.email == email).all()
    if otp_records:
        for otp_record in otp_records:
            delete(otp_record, db)
    code = ''.join(random.choices('1234567890',k=6))
    otp_rec = otpmodel.OTP(
        code = code,
        email = email
    )
    create(otp_rec, db)
    return code


def send_mail(email,code):
    sender_mail = Config.SENDER_MAIL
    receiver_mail = email
    password = Config.PASSWORD

    message = MIMEMultipart()
    message["From"] = sender_mail
    message["To"] = receiver_mail
    message["Subject"] = "OTP for user verification"

    body = f"Your OTP is : {code}"
    message.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    server.starttls()
    server.login(sender_mail, password)
    server.sendmail(sender_mail, receiver_mail, message.as_string())


def verify_otp(code, email, db):
    otp_record = db.query(otpmodel.OTP).filter(otpmodel.OTP.email == email).first()

    time = datetime.now()
    if otp_record and otp_record.code == code and otp_record.created_at + timedelta(minutes=2)  >= time :
        db.query(otpmodel.OTP).filter(otpmodel.OTP.email == email).delete(synchronize_session=False)
        db.commit()
        return True
    else: 
        return False

