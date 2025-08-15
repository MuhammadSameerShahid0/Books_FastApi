import datetime
import os

import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def create_jwt(data: dict):
    to_encode = data.copy()
    expires = datetime.datetime.now() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expires})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return access_token