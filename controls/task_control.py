# -- interno --
from classes.user_class import User
from classes.task_class import Task
from db.db_tools import exists_in_db
from exceptions.exceptions import UserExists
from session.session import with_session
# -- externo --
import asyncio
import sqlite3
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


# Criar tarefa
@with_session
def task_create(session: Session, title: str, description: str, due: str, user_id: int) -> None:
    # if exists_in_db(Usuario, nome = nome): raise UsuarioExistente(nome)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    try:
        task = Task(title = title, description = description, due = due, user_id = user_id)
        session.add(task)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()


# Editar tarefa - BREVE


# Remover tarefa
@with_session
def task_remove(session: Session, task_id: int) -> None:
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()


# Listar todas as terefas de um usuário
@with_session
def list_user_tasks(session: Session, user_id: int) -> List[Task]:
    return session.query(Task).filter_by(user = user_id).all()


# Listar todas as tarefas
@with_session
def list_all_tasks(session: Session) -> List[Task]:
    return session.query(Task).all()


#async def main():
#    await nova_tarefa('Sagunda Tarefa', 'Completar segunda Tarefa', 1)


#if __name__ == '__main__':
#    asyncio.run(main())

