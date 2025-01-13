import os
from dotenv import load_dotenv
from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(database_url)
connect_args = {}
engine = create_engine(database_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session
        

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
 
        
SessionDep = Annotated[Session, Depends(get_session)]
