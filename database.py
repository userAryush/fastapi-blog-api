from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
MYSQL_URL = "mysql+pymysql://root:Aryush%401234K@localhost/blog_api"

engine = create_engine(MYSQL_URL)

SessionLocal = sessionmaker(autocommit = False, bind = engine)

Base = declarative_base()