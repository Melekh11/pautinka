"""
    This module contains the user routes. The user routes handle user registration, login, and profile management.
    
    Attributes:
        user_router (APIRouter): The FastAPI router for the user routes.
        SECRET_KEY (str): The secret key for JWT token encoding.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for JWT tokens.
        HASH_ALGORITHM (str): The hashing algorithm for passwords.
        logger (Logger): The logger for the user routes.
        pwd_context (CryptContext): The password hashing context.
        oauth2_scheme (OAuth2PasswordBearer): The OAuth2 password bearer for token authentication.
        
    Functions:
        get_password_hash(password) -> str: Hashes a plain password.
        verify_password(plain_password, hashed_password) -> bool: Verifies a plain password against a hashed password.
        create_access_token(data, expires_delta) -> str: Creates a JWT access token.
        get_current_user(token, session) -> ResponseUser: Retrieves the current authenticated user from the token.
        register(session, user_data) -> Token: Registers a new user and returns an access token.
        token(user_data, session) -> Token: Authenticates a user and returns an access token.
        me(current_user) -> ResponseUser: Retrieves the current authenticated user's details.
        get_user(user_id, session) -> ResponseUser: Retrieves a user's details by user ID.
        me(session, edited_user, current_user) -> str: Updates the current authenticated user's details.
        create_review(session, review_data, current_user) -> str: Creates a new work review.
        search_user_by_tags(tags, session) -> list[ResponseUser]: Searches for users by tags.
"""

import os
import logging
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from database import SessionDep, select
from models.users import TagsUsers, Tags, Users
from shemas.user import EditedUser, RegisterUser, LoggingUser, ResponseUser, WorkReview
from helpers.crud import (
    create_workreview,
    get_user_by_email,
    get_user_by_phone,
    get_user_by_id,
    create_user,
)

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")


logger = logging.getLogger("user_router")
logger.setLevel("DEBUG")


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


class Token(BaseModel):
    """
        Represents the token response model.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the data contained in a JWT token.
    """
    id: int


def get_password_hash(password) -> str:
    """
    Hashes a plain password.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta): The token expiration time.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> ResponseUser:
    """
    Retrieves the current authenticated user from the token.

    Args:
        token (str): The JWT token.
        session (SessionDep): The database session.

    Returns:
        ResponseUser: The current authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    bad_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: str = payload.get("user-id")
        if user_id is None:
            raise bad_token_exception
        user_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise bad_token_exception
    user = get_user_by_id(id=user_data.id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no such login",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_router.post("/register", response_model=Token)
async def register(session: SessionDep, user_data: RegisterUser) -> Token:

    if user_data.email != "":

        same_email = get_user_by_email(email=user_data.email, session=session)

        if same_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email exists",
                headers={"WWW-Authenticate": "Bearer"},
            )

    if user_data.phone != "":
        same_phone = get_user_by_phone(phone=user_data.phone, session=session)

        if same_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="phone exists",
                headers={"WWW-Authenticate": "Bearer"},
            )

    new_user = create_user(
        user=user_data, hashed_password=get_password_hash(user_data.password)
    )
    session.add(new_user)
    session.commit()
    logger.info(f"new user {new_user.name} created")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_token = create_access_token(
        data={"user-id": new_user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=user_token, token_type="bearer")


@user_router.post("/token", response_model=Token)
async def token(
    user_data: LoggingUser,
    session: SessionDep,
) -> Token:
    """
    Authenticate a user and return an access token.
    
    Args:
        user_data (LoggingUser): The user's login data.
        session (SessionDep): The database session.
        
    Returns:
        Token: The access token.
    """
    if not (user_data.email or user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not enough data",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_data.email:
        user = get_user_by_email(email=user_data.email, session=session)
    elif user_data.phone:
        user = get_user_by_phone(phone=user_data.phone, session=session)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not valid data",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no such login",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"user {user.name} successfully logged")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_token = create_access_token(
        data={"user-id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=user_token, token_type="bearer")


@user_router.get("/me", response_model=ResponseUser)
async def me(current_user: Annotated[ResponseUser, Depends(get_current_user)]) -> ResponseUser:
    """
    Retrieve the current authenticated user's details.

    Args:
        current_user (ResponseUser): The current authenticated user.

    Returns:
        ResponseUser: The current user's details.
    """
    return current_user


@user_router.get("/{user_id}", response_model=ResponseUser)
def get_user(user_id: int, session: SessionDep) -> ResponseUser:
    """
    Retrieve a user's details by user ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        session (SessionDep): The database session.

    Returns:
        ResponseUser: The user's details.
    """
    return get_user_by_id(id=user_id, session=session)


@user_router.patch("/me")
async def me(
    session: SessionDep,
    edited_user: EditedUser,
    current_user: Annotated[ResponseUser, Depends(get_current_user)],
) -> str:
    """
    Update the current authenticated user's details.

    Args:
        session (SessionDep): The database session.
        edited_user (EditedUser): The user data to update.
        current_user (ResponseUser): The current authenticated user.

    Returns:
        str: Status message.
    """
    for key in edited_user.model_fields_set:
        current_user[key] = edited_user[key]

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return "success"


@user_router.post("/workreview")
async def create_review(
    session: SessionDep,
    review_data: WorkReview,
    current_user: Annotated[ResponseUser, Depends(get_current_user)],
) -> str:
    """
    Create a new work review.

    Args:
        session (SessionDep): The database session.
        review_data (WorkReview): The work review data.
        current_user (ResponseUser): The current authenticated user.

    Returns:
        str: Success message.
    """
    new_review = create_workreview(review_data, current_user.id)

    session.add(new_review)
    session.commit()
    return "success"


@user_router.get("/search/{tags}", response_model=list[ResponseUser])
async def search_user_by_tags(tags: str, session: SessionDep) -> list[ResponseUser]:
    """
    Search for users by tags.

    Args:
        tags (str): Comma-separated list of tags to search for.
        session (SessionDep): The database session.

    Returns:
        list[ResponseUser]: List of users matching the tags.
    """
    tag_list = tags.split(",")
    users = session.exec(
        select(Users)
        .join(TagsUsers)
        .join(Tags)
        .where(Tags.name.in_(tag_list))
    ).all()
    return users
