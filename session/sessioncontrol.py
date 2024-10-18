# -- interno --

# -- externo --
from typing import Any
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Base
b = declarative_base()


# Gerar tebelas
def criar_tabelas(engine: Engine) -> None:
    b.metadata.create_all(engine)


# Gerenciador de sessão
def with_session(func: callable) -> any:
    @wraps(func)
    def wrapper(*args, **kwargs) -> any:
        # Conectando DB
        engine = create_engine('sqlite:///db/todolist.db', echo = True)

        # Gerar tabela não existente
        criar_tabelas(engine)

        # Sessão banco
        Session = sessionmaker(bind = engine)
        session = Session()
        
        # serviço
        servico = func(session, *args, **kwargs)

        # Fechar sessão
        session.close()

        return servico
    
    return wrapper

