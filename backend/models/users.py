from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

class TagsUsers(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)


class Subscription(SQLModel, table=True):
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


class Users(SQLModel, table=True):
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
    
    subscribers: list["Subscription"] = Relationship(back_populates="user_to", sa_relationship_kwargs={
            "foreign_keys": "Subscription.user_id_from",
            "lazy": "selectin",
        },
    )
    followers: list["Subscription"] = Relationship(back_populates="user_from", sa_relationship_kwargs={
            "foreign_keys": "Subscription.user_id_to",
            "lazy": "selectin",
        },
    )
    tags: list["Tags"] = Relationship(back_populates="users", link_model=TagsUsers)
    workreviews: list["Workreviews"] = Relationship(back_populates="user")


class Tags(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    users: list["Users"] = Relationship(back_populates="tags", link_model=TagsUsers)


class Workreviews(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    post: str
    date_start: date = Field(default=datetime.now)
    date_end: Optional[date]
    company_name: str
    subcompany_name: Optional[str]

    user_id: int = Field(foreign_key="users.id")
    user: "Users" = Relationship(back_populates="workreviews")
