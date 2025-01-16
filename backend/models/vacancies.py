from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from models.users import Users


class Vacancy(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    conditions: str
    vacancy_holder_id: int = Field(foreign_key="users.id")
    related_project: Optional[str] = None
    
    vacancy_holder = Optional["Users"] = Relationship(back_populates="vacancies")