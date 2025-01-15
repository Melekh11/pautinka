import os
import logging
from dotenv import load_dotenv
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlmodel import create_engine, Session, SQLModel

load_dotenv(override=True)

logger = logging.getLogger("db")
logger.setLevel("DEBUG")

database_url = URL.create(
    "postgresql",
    username=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host="localhost",
    port="5432",
    database="postgres_database",
)
connect_args = {}

engine = create_engine(database_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("tables created")


SessionDep = Annotated[Session, Depends(get_session)]
