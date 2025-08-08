from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Settings

settings = Settings()

MYSQL_URL = settings.DATABASE_URL

engine = create_engine(MYSQL_URL)

SessionLocal = sessionmaker(autocommit = False, bind = engine)

Base = declarative_base()