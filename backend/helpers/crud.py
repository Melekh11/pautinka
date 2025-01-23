from sqlmodel import select

from ..database import SessionDep
from ..models.users import Users as UserModel, Workreviews as WorkreviewModel
from ..schemas.user import RegisterUser, WorkReview


def get_user_by_email(email: str, session: SessionDep) -> UserModel | None:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user.
        session (SessionDep): The database session.

    Returns:
        UserModel | None: The user with the specified email address, or None if not found.
    """
    return session.exec(select(UserModel).where(UserModel.email == email)).first()


def get_user_by_phone(phone: str, session: SessionDep) -> UserModel | None:
    """
    Retrieve a user by their phone number.

    Args:
        phone (str): The phone number of the user.
        session (SessionDep): The database session.

    Returns:
        UserModel | None: The user with the specified phone number, or None if not found.
    """
    return session.exec(select(UserModel).where(UserModel.phone == phone)).first()


def get_user_by_id(id: int, session: SessionDep) -> UserModel | None:
    """
    Retrieve a user by their ID.

    Args:
        id (int): The ID of the user.
        session (SessionDep): The database session.

    Returns:
        UserModel | None: The user with the specified ID, or None if not found.
    """
    return session.exec(select(UserModel).where(UserModel.id == id)).first()


def create_user(user: RegisterUser, hashed_password: str) -> UserModel:
    """
    Create a new user.

    Args:
        user (RegisterUser): The user data.
        hashed_password (str): The hashed password of the user.

    Returns:
        UserModel: The newly created user.
    """
    new_user = UserModel(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password,
    )

    return new_user


def create_workreview(review: WorkReview, owner_id: int) -> WorkreviewModel:
    """
    Create a new work review.

    Args:
        review (WorkReview): The work review data.
        owner_id (int): The ID of the user who owns the review.

    Returns:
        WorkreviewModel: The newly created work review.
    """
    new_review = WorkreviewModel(
        post=review.post,
        date_start=review.date_start,
        date_end=review.date_end,
        company_name=review.company_name,
        subcompany_name=review.subcompany_name,
        user_id=owner_id,
    )

    return new_review
