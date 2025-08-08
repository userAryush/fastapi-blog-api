from sqlalchemy import Integer, Column, String
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String(50), unique = True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    
