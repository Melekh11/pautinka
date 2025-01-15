from typing import Annotated, Optional, ClassVar
from datetime import date

from pydantic import BaseModel


class LoggingUser(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    password: str


class RegisterUser(LoggingUser):
    name: str
    surname: str
    

class ResponseUser(BaseModel):
    id: int
    name: Optional[str]
    surname: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    university: Optional[str]
    birthdate: Optional[date]
    course: Optional[str]
    short_status: Optional[str]
    full_status: Optional[str]
    about_me: Optional[str]
    links: Optional[str]


class EditedUser(ResponseUser):
    pass
    
    
class WorkReview(BaseModel):
    post: str
    date_start: Optional[date]
    date_end: Optional[date]
    company_name: str
    subcompany_name: Optional[str]
