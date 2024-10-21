# -- INTERNO --
from session.base import b
# -- EXTERNO --
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, DateTime, Boolean


# Classe usuários
class User(b):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    active = Column(Boolean, default = True) # Alterar default para False futuramente
    
    # Relacionamento com "Task"
    tasks = relationship('Task', back_populates = 'user')

    # Retorna se o usuário está autenticado ou não
    def is_authenticated(self) -> bool:
        return True


    # Conta ativa (para validar criação de contas futuramente)
    def is_active(self) -> bool:
        return self.active


    # Retornar ID
    def get_id(self) -> int:
        return self.id

