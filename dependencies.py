from database import SessionLocal
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth import decode_token
from models import Users
from jose import JWTError

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2), db:Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(Users).filter(Users.username == payload["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
          
        
        
