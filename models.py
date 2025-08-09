from sqlalchemy import Integer, Column, String, ForeignKey, DateTime,func
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique = True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    
    posts = relationship("Blog", back_populates="author")
    
class Blog(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(1000))
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    author = relationship("Users", back_populates="posts")