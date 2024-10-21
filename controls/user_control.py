# -- interno --
from classes.user_class import User
from classes.task_class import Task
from db.db_tools import exists_in_db
from exceptions.exceptions import UserExists, UserNotFound
from session.session import with_session
# -- externo --
import bcrypt
import asyncio
import sqlite3
from sqlalchemy.orm import Session

# Registrar usuário
@with_session
async def user_add(session: Session, name: str, password: str, email: str) -> None:
    if exists_in_db(User, email = email): raise UserExists(email)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    # Gerando hash da senha
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = User(name = name, password = hashed, email = email)
    session.add(user)
    session.commit()


# Editar usuário
@with_session
async def user_edit(session: Session, id: int, new_name: str, new_password: str, new_email: str) -> None:
    if not exists_in_db(User, id = id): raise excecoes.UserInexistente(f'ID {id}')
    if exists_in_db(User, name = new_name): raise UserExists(name)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    # Gerando hash da senha
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    user = session.query(User).filter_by(id = id).first()
    if usuario:
        user.name = new_name
        user.email = new_email
        user.password = hashed
        session.commit()


# Remover usuário
@with_session
async def user_remove(session: Session, name: str) -> None:
    if not exists_in_db(User, name = name): raise UserNotFound(name)
    user = session.query(User).filter_by(name = name).first()
    session.delete(user)
    session.commit()


# Listar usuários
@with_session
async def user_list(session: Session) -> list[User]:
    return session.query(User).all()


#async def main():
#    await cadastrar_usuario('User', 'senha', 'user@mail.com')


#if __name__ == '__main__':
#    asyncio.run(main())

