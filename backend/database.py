# database.py
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///cbt.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from models import Message, Policy
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
