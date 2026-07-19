

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os 

load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session_Local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()