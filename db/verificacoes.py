# -- interno --
from session.sessioncontrol import with_session
# -- externo --
from sqlalchemy.orm import Session


@with_session
def registro_existe(session: Session, classe: str, **kwargs) -> bool:
    registro_existente = session.query(classe).filter_by(**kwargs).first()
    if registro_existente: return True
    else: False

