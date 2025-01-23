"""
This module defines the SQLModel models for the application, including the Users model,
the many-to-many relationship between users and tags (TagsUsers), and the many-to-many
relationship for user subscriptions (Subscription).
"""

from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TagsUsers(SQLModel, table=True):
    """
    Represents the many-to-many relationship between users and tags.
    """
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)


class Subscription(SQLModel, table=True):
    """
    Represents the many-to-many relationship for user subscriptions.
    """
    user_id_from: int = Field(foreign_key="users.id", primary_key=True)
    user_from: "Users" = Relationship(
        back_populates="subscribers",
        sa_relationship_kwargs={"foreign_keys": "Subscription.user_id_from"},
    )

    user_id_to: int = Field(foreign_key="users.id", primary_key=True)
    user_to: "Users" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "Subscription.user_id_to"},
    )

class Vacancy(SQLModel, table=True):
    """
    Represents a job vacancy.
    """
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    conditions: str
    vacancy_holder_id: int = Field(foreign_key="users.id")
    related_project: Optional[str] = None
    vacancy_holder = Optional["Users"] = Relationship(back_populates="vacancies")

class Likes(SQLModel, table=True):
    """
    Represents the many-to-many relationship for likes between users.
    """
    user_id_from: int = Field(foreign_key="users.id", primary_key=True)
    user_from: "Users" = Relationship(
        back_populates="likes",
        sa_relationship_kwargs={"foreign_keys": "Likes.user_id_from"},
    )

    user_id_to: int = Field(foreign_key="users.id", primary_key=True)
    user_to: "Users" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "Likes.user_id_to"},
    )
class Users(SQLModel, table=True):
    """
    Represents a user in the system.
    """
    id: int = Field(default=None, primary_key=True)
    name: str
    surname: str
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    university: Optional[str]
    birthdate: Optional[date]
    course: Optional[str]
    short_status: Optional[str]
    full_status: Optional[str]
    about_me: Optional[str]
    links: Optional[str]

    hashed_password: Optional[str]

    subscribers: list["Subscription"] = Relationship(
        back_populates="user_to",
        sa_relationship_kwargs={
            "foreign_keys": "Subscription.user_id_from",
            "lazy": "selectin",
        },
    )
    followers: list["Subscription"] = Relationship(
        back_populates="user_from",
        sa_relationship_kwargs={
            "foreign_keys": "Subscription.user_id_to",
            "lazy": "selectin",
        },
    )
    
    likes: list["Likes"] = Relationship(back_populates="user")
    
    tags: list["Tags"] = Relationship(back_populates="users", link_model=TagsUsers)
    workreviews: list["Workreviews"] = Relationship(back_populates="user")

    vacancies: list["Vacancy"] = Relationship(back_populates="vacancy_holder")

class Tags(SQLModel, table=True):
    """
    Represents a tag that can be associated with a user.
    """
    id: int = Field(default=None, primary_key=True)
    name: str

    users: list["Users"] = Relationship(back_populates="tags", link_model=TagsUsers)


class Workreviews(SQLModel, table=True):
    """
    Represents a work review for a user.
    """
    id: int = Field(default=None, primary_key=True)
    post: str
    date_start: date = Field(default=datetime.now)
    date_end: Optional[date]
    company_name: str
    subcompany_name: Optional[str]

    user_id: int = Field(foreign_key="users.id")
    user: "Users" = Relationship(back_populates="workreviews")
