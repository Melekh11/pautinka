from sqlmodel import select

from database import SessionDep
from models.users import Users as UserModel, Workreviews as WorkreviewModel
from shemas.user import RegisterUser, WorkReview


def get_user_by_email(email: str, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel).where(UserModel.email == email)).first()


def get_user_by_phone(phone: str, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel).where(UserModel.phone == phone)).first()


def get_user_by_id(id: int, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel).where(UserModel.id == id)).first()


def create_user(user: RegisterUser, hashed_password: str) -> UserModel:
    new_user = UserModel(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password,
    )

    return new_user


def create_workreview(review: WorkReview, owner_id: int) -> WorkreviewModel:
    new_review = WorkreviewModel(
        post=review.post,
        date_start=review.date_start,
        date_end=review.date_end,
        company_name=review.company_name,
        subcompany_name=review.subcompany_name,
        user_id=owner_id,
    )

    return new_review
