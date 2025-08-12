from pydantic import BaseModel,EmailStr
from typing import List, Optional
class CreateUser(BaseModel):
    username:str
    email:EmailStr
    password:str
    
    model_config = {"extra":"forbid"}
    
class LoginUser(BaseModel):
    email:EmailStr
    password:str
    
    
    model_config = {"extra":"forbid"}
    
class CreateBlog(BaseModel):
    title:str
    content:str
    tag_ids: Optional[List[int]] = []
    
    
    model_config = {"extra":"forbid"}
    
class CreateComment(BaseModel):
    content:str
    blog_id:int
    
    model_config = {"extra":"forbid"}
    
class UpdateComment(BaseModel):
    content: str
    model_config = {"extra":"forbid"}
    
class CreateTag(BaseModel):
    name:str
    model_config = {"extra":"forbid"}