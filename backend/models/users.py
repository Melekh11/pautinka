from typing import Optional

from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    login: Optional[str] = Field(index=True)
    name: str
    surname: str
    phone: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
