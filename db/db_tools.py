# -- interno --
from session.session import with_session
from classes.user_class import User
# -- externo --
from sqlalchemy.orm import Session


@with_session
def exists_in_db(session: Session, classe: str, **kwargs) -> bool:
    exists = session.query(classe).filter_by(**kwargs).first()
    return True if exists else False


@with_session
def get_user(session: Session, email: str) -> str:
    return session.query(User).filter_by(email = email).first()

