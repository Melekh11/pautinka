from datetime import timedelta
import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..database import SessionDep
from ..schemas.user import RegisterUser, LoggingUser
from ..helpers.crud import get_user_by_email, get_user_by_phone, create_user
from ..utils.security import get_password_hash, verify_password, create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

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

@auth_router.post("/register", response_model=Token)
async def register(session: SessionDep, user_data: RegisterUser) -> Token:
    """
    Registers a new user and returns an access token.

    Args:
        session (SessionDep): The database session.
        user_data (RegisterUser): The registration data for the user.

    Returns:
        Token: The access token.
    """
    if user_data.email:
        if get_user_by_email(email=user_data.email, session=session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email exists",
            )

    if user_data.phone:
        if get_user_by_phone(phone=user_data.phone, session=session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="phone exists",
            )

    new_user = create_user(user=user_data, hashed_password=get_password_hash(user_data.password))
    session.add(new_user)
    session.commit()

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token = create_access_token(data={"user-id": new_user.id}, expires_delta=access_token_expires)
    return Token(access_token=token, token_type="bearer")


@auth_router.post("/token", response_model=Token)
async def token(session: SessionDep, user_data: LoggingUser) -> Token:
    """
    Authenticate a user and return an access token.

    Args:
        user_data (LoggingUser): The user's login data.
        session (SessionDep): The database session.

    Returns:
        Token: The access token.
    """
    user = None
    if user_data.email:
        user = get_user_by_email(email=user_data.email, session=session)
    elif user_data.phone:
        user = get_user_by_phone(phone=user_data.phone, session=session)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    _token = create_access_token(data={"user-id": user.id}, expires_delta=access_token_expires)
    return Token(access_token=_token, token_type="bearer")
