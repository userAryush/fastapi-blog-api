# pip install pydantic_settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    ALGORITHM : str
    TOKEN_EXPIRY_MINUTE:int
    SECRET_KEY: str
    
    model_config = {'env_file':'.env'}
    
