from typing import Annotated, Optional

from pydantic import BaseModel


class LoggingUser(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    password: str


class RegestratingUser(LoggingUser):
    name: str
    surname: str
    

class User(BaseModel):
    id: int
    login: str
    name: Optional[str]
    surname: Optional[str]
