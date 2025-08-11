from sqlalchemy import Integer, Column, String, ForeignKey, DateTime,func
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique = True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    
    # One user can have many posts
    posts = relationship("Blog", back_populates="author")
    # One user can have many comments
    comments = relationship("Comments", back_populates="user")

    
class Blog(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(1000))
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    author = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="post")
    
class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("Users", back_populates="comments")
    post = relationship("Blog", back_populates="comments")