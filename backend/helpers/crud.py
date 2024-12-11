from sqlmodel import select

from database import SessionDep
from models.users import Users as UserModel
from shemas.user import RegestratingUser

def get_user_by_email(email: str, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel)
                        .where(UserModel.email == email)).first()


def get_user_by_phone(phone: str, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel)
                        .where(UserModel.phone == phone)).first()


def get_user_by_id(id: int, session: SessionDep) -> UserModel | None:
    return session.exec(select(UserModel).where(UserModel.id == id)).first()


def create_user(user: RegestratingUser, hashed_password: str) -> UserModel:
    new_user = UserModel(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password
    )
    
    return new_user