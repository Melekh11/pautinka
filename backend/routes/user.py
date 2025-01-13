import os
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from database import SessionDep
from shemas.user import EditedUser, RegestratingUser, LoggingUser, User, WorkReview
from helpers.crud import get_user_by_email, get_user_by_phone, get_user_by_id, create_user, create_workreview

SECRET_KEY = "qwerty"
user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
    ) -> User:
    bad_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(token)
        print("ok lets do it")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        print("payload", payload)
        user_id: str = payload.get("user-id")
        print("ok got user id", user_id)
        if user_id is None:
            print("cant read jwt")
            raise bad_token_exception
        
        user_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise bad_token_exception
    user = get_user_by_id(id=user_data.id, session=session)
    print("hahaha hot user", user)
    if not user:
        print("no user with such id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no such login",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_router.post("/register", response_model=Token)
async def register(
    session: SessionDep,
    user_data: RegestratingUser
):
        
    if user_data.email != "":
        
        same_email = get_user_by_email(
            email=user_data.email,
            session=session
        )
        
        print(same_email)
        if same_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email exists",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    if user_data.phone != "":
        same_phone = get_user_by_phone(
            phone=user_data.phone,
            session=session
        )
        
        if same_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="phone exists",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    # print(get_password_hash(user_data.password))
    new_user = create_user(user=user_data, hashed_password=get_password_hash(user_data.password))
    session.add(new_user)
    session.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_token = create_access_token(
        data={"user-id": new_user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=user_token, token_type="bearer")


@user_router.post("/token", response_model=Token)
async def token(
    user_data: LoggingUser,
    session: SessionDep,
):
    user = RegestratingUser(
        name="qqq",
        surname="qqq",
        phone="111",
        email="111",
        password="qqq"
    )
    new_user = create_user(user, get_password_hash("qqq"))
    session.add(new_user)
    session.commit()

    print(user_data)
    if not (user_data.email or user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not enough data",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_data.email:
        user = get_user_by_email(
            email=user_data.email,
            session=session
        )
    else:
        user = get_user_by_phone(
            phone=user_data.phone,
            session=session
        )

    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="no such login",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    print(verify_password(user_data.password, user.hashed_password))
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_token = create_access_token(
        data={"user-id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=user_token, token_type="bearer")


@user_router.get("/me", response_model=User)
async def me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@user_router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep):
    return get_user_by_id(id=user_id, session=session)


@user_router.patch("/me")
async def me(
     session: SessionDep,
     edited_user: EditedUser,
     current_user: Annotated[User, Depends(get_current_user)],
):
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
    current_user: Annotated[User, Depends(get_current_user)],
):
    new_review = create_workreview(review_data, current_user.id)
    
    session.add(new_review)
    session.commit()
    return "success"
