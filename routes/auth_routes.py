from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateUser, LoginUser
from dependencies import get_db
from sqlalchemy.orm import Session
from models import Users
from sqlalchemy import or_
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup",status_code=status.HTTP_201_CREATED)
def signup(user:CreateUser,db:Session=Depends(get_db)):
    existing_user = db.query(Users).filter(or_(user.username == Users.username, user.email == Users.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "User with this name or email already exists!")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)  # hash before saving
    
    new_user = Users(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail":"New user created successfully!!","username":user.username,"email":user.email}    

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user:LoginUser, db:Session=Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials!")
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")
    
    token = create_access_token({"email":existing_user.email, "username":existing_user.username})
    return {"detail":"Logged in successfully!!","token_type":"Bearer","token":token}


    