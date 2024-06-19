import jwt
from datetime import datetime, timedelta, timezone
from entities.userBase import UserBase
import os
from dotenv import load_dotenv

load_dotenv()

def encode(data: UserBase):
    secret = os.getenv('SECRET')
    expiração = datetime.now(timezone.utc) + timedelta(minutes=720)

    payload = {"sub": data.matricula, "exp": expiração}

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def decode(token):
    secret = os.getenv('SECRET')
    return jwt.decode(token, secret, algorithms=['HS256'])