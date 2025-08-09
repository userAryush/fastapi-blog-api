from jose import jwt
from passlib.context import CryptContext
from config import Settings
from datetime import datetime, timedelta, timezone

settings = Settings()

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
TOKEN_EXPIRT_MINUTE = settings.TOKEN_EXPIRY_MINUTE

pwd_context = CryptContext(schemes="bcrypt",deprecated ="auto")

def hash_password(raw_password:str):
    return pwd_context.hash(raw_password)

def verify_password(raw_password:str, hashed_password:str):
    return pwd_context.verify(raw_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token:str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])