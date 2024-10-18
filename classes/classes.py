from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin
from datetime import datetime


# Base
b = declarative_base()


# Classe usuários
class Usuario(b):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True)
    nome = Column(String, unique = True, nullable = False)
    senha = Column(String, nullable = False)
    email = Column(String, nullable = False)
    tarefas = relationship('Tarefa', back_populates = 'usuario')


    # Retorna se o usuário está autenticado ou não
    def is_authenticated(self) -> bool:
        return True


    # Conta ativa
    def is_active(self) -> bool:
        return True


    # Retornar ID
    def get_id(self) -> str:
        return str(self.id)


# Classe tarefa
class Tarefa(b):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key = True)
    titulo = Column(String, nullable = False)
    descricao = Column(String, nullable = False)
    data_criacao = Column(DateTime, default = datetime.now)
    data_prazo = Column(DateTime)
    #data_prazo = Column(String, nullable = False)
    concluida = Column(Boolean, default = False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates = 'tarefas')

