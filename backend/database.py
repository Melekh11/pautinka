"""
This module sets up the database connection and provides utility functions for the application.

The following functionalities are included:
- Loading environment variables using dotenv.
- Configuring the database connection URL and creating the SQLAlchemy engine.
- Setting up the password hashing context using Passlib.
- Providing a function to get a database session for dependency injection.
- Creating the database tables and initializing the default root user if not present.
"""
import os
import logging

from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import URL, select
from sqlmodel import create_engine, Session, SQLModel
from passlib.context import CryptContext

from .models.users import Users


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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    """
    Provides a database session for dependency injection.
    
    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """
    Creates database tables and a default root user if it does not exist.
    
    This function initializes the database schema by creating all tables defined
    in the SQLModel metadata. It also checks if a root user exists, and if not,
    creates one with the credentials specified in the environment variables.
    """
    SQLModel.metadata.create_all(engine)
    logger.info("tables created")

    with Session(engine) as session:
        _root_user_name = os.getenv("ROOT_NAME")
        _root_user_surname = os.getenv("ROOT_SURNAME")
        _root_user_password = os.getenv("ROOT_PASSWORD")
        root_user = session.exec(select(Users).where(Users.name == _root_user_name)).first()
        if not root_user:
            hashed_password = pwd_context.hash(_root_user_password)
            new_user = Users(
                name=_root_user_name,
                surname=_root_user_surname,
                email=None,
                phone=None,
                hashed_password=hashed_password
            )
            session.add(new_user)
            session.commit()
            logger.info("Default root user created")

SessionDep = Annotated[Session, Depends(get_session)]
