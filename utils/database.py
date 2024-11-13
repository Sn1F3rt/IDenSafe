from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{user}:{pw}@{host}:{port}/{db}".format(
    user=DB_USER, pw=DB_PASS, host=DB_HOST, port=DB_PORT, db=DB_NAME
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=100,
    pool_recycle=120,
    pool_pre_ping=True,
    max_overflow=0,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_session():
    return SessionLocal()
