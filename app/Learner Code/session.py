from sqlalchemy import create_engine , Session 
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine


engine = create_engine("sqlite:///products.db",echo=True,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

