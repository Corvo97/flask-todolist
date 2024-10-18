# -- interno --
from excecoes.excecoes import CampoEmBranco
from classes.classes import Usuario, Tarefa
from db.verificacoes import registro_existe
from excecoes.excecoes import UsuarioExistente
from session.sessioncontrol import with_session
# -- externo --
import bcrypt
import asyncio
import sqlite3
from sqlalchemy.orm import Session

# Registrar usuário
@with_session
async def cadastrar_usuario(session: Session, nome: str, senha: str, email: str) -> None:
    if registro_existe(Usuario, nome = nome): raise UsuarioExistente(nome)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    # Gerando hash da senha
    hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    usuario = Usuario(nome = nome, senha = hashed, email = email)
    session.add(usuario)
    session.commit()


# Editar usuário
@with_session
async def editar_usuario(session: Session, id: int, novo_nome: str, nova_senha: str, novo_email: str) -> None:
    if not registro_existe(Usuario, id = id): raise excecoes.UsuarioInexistente(f'ID {id}')
    if registro_existe(Usuario, nome = novo_nome): raise UsuarioExistente(novo_nome)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    # Gerando hash da senha
    hashed = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

    usuario = session.query(Usuario).filter_by(id = id).first()
    if usuario:
        usuario.nome = novo_nome
        usuario.email = novo_email
        usuario.senha = hashed
        session.commit()


# Remover usuário
@with_session
async def remover_usuario(session: Session, nome: str) -> None:
    if not registro_existe(Usuario, nome = nome): raise excecoes.UsuarioInexistente(nome)
    usuario = session.query(Usuario).filter_by(nome = nome).first()
    session.delete(usuario)
    session.commit()


# Listar usuários
@with_session
async def listar_usuarios(session: Session) -> list[Usuario]:
    return session.query(Usuario).all()


#async def main():
#    await cadastrar_usuario('Usuario', 'senha', 'user@mail.com')


#if __name__ == '__main__':
#    asyncio.run(main())

