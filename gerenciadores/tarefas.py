# -- interno --
from classes.classes import Usuario, Tarefa
from db.verificacoes import registro_existe
from excecoes.excecoes import UsuarioExistente
from session.sessioncontrol import with_session
# -- externo --
import asyncio
import sqlite3
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


# Criar tarefa
@with_session
def adicionar_tarefa(session: Session, titulo: str, descricao: str, data_prazo: str, usuario_id: int) -> None:
    # if registro_existe(Usuario, nome = nome): raise UsuarioExistente(nome)
    # -- FILTRO EMAIL EXISTENTE --
    # -- FILTRAR TAMANHO E FORMATO DE SENHA --

    try:
        tarefa = Tarefa(titulo = titulo, descricao = descricao, usuario_id = usuario_id, data_prazo = data_prazo)
        session.add(tarefa)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()


# Editar tarefa - BREVE


# Remover tarefa
@with_session
def deletar_tarefa(session: Session, tarefa_id: int) -> None:
    # if not registro_existe(Usuario, nome = nome): raise UsuarioInexistente(nome)
    tarefa = session.query(Tarefa).get(tarefa_id)
    if tarefa:
        session.delete(tarefa)
        session.commit()


# Listar todas as terefas de um usuário
@with_session
def listar_tarefas_do_usuario(session: Session, usuario_id: int) -> List[Tarefa]:
    return session.query(Tarefa).filter_by(usuario_id = usuario_id).all()


# Listar todas as tarefas
@with_session
def listar_todas_as_tarefas(session: Session) -> List[Tarefa]:
    return session.query(Tarefa).all()


#async def main():
#    await nova_tarefa('Sagunda Tarefa', 'Completar segunda Tarefa', 1)


#if __name__ == '__main__':
#    asyncio.run(main())

