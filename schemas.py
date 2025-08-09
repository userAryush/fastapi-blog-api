from pydantic import BaseModel,EmailStr

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
    
    model_config = {"extra":"forbid"}