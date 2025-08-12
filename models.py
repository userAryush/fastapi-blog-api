from sqlalchemy import Integer, Column, String, ForeignKey, DateTime,func
from sqlalchemy.orm import relationship
from database import Base

class PostLike(Base):
    __tablename__ = 'post_likes'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship('User', back_populates='likes', ondelete="CASCADE")
    post = relationship('Post', back_populates='likes', ondelete="CASCADE")
    
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
    # One user can have many likes
    likes = relationship("PostLike", back_populates="user")

class BlogTag(Base):
    __tablename__ = 'blog_tag'
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey('posts.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    
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
    tags = relationship("Tags", secondary='blog_tag', back_populates="posts")
    likes = relationship("PostLike", back_populates="post")
    
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
    
class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    posts = relationship("Blog", secondary='blog_tag', back_populates="tags")
    
