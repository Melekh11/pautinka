from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import select

from ..models.users import Users, TagsUsers, Tags
from ..database import SessionDep
from ..schemas.user import WorkReview, ResponseUser
from ..helpers.crud import create_workreview
from ..utils.security import get_current_user

review_router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@review_router.post("/workreview")
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


@review_router.get("/search/{tags}", response_model=list[ResponseUser])
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
