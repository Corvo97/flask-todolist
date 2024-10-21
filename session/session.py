# -- interno --
from session.base import b
# -- externo --
from typing import Any
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE = 'todolist.db'


# Gerar tebelas
def create_tables(engine: Engine) -> None:
    b.metadata.create_all(engine)


# Gerenciador de sessão
def with_session(func: callable) -> any:
    @wraps(func)
    def wrapper(*args, **kwargs) -> any:
        # Conectando DB
        engine = create_engine(f'sqlite:///db/{DATABASE}', echo = True)

        # Gerar tabela não existente
        create_tables(engine)

        # Sessão banco
        Session = sessionmaker(bind = engine)
        session = Session()
        
        # serviço
        task = func(session, *args, **kwargs)

        # Fechar sessão
        session.close()

        return task
    
    return wrapper

