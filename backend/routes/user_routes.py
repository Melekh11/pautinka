from typing import Annotated
from fastapi import APIRouter, Depends

from ..database import SessionDep
from ..schemas.user import EditedUser, ResponseUser
from ..helpers.crud import get_user_by_id
from ..utils.security import get_current_user

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

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
    return get_user_by_id(user_id, session=session)


@user_router.patch("/me")
async def update_user(
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
        setattr(current_user, key, getattr(edited_user, key))
    session.add(current_user)
    session.commit()
    return "success"
