# -- interno --
from classes.classes import Usuario, Tarefa
from session.sessioncontrol import with_session
# -- externo --
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from flask_login import current_user
from sqlalchemy.orm import joinedload


@with_session
def trazer_usuario(session: Session, nome: str) -> str:
    return session.query(Usuario).options(joinedload(Usuario.tarefas)).filter_by(nome = nome).first()

@with_session
def trazer_dono_tarefa(session: Session, id: int) -> int:
    tarefa = session.query(Tarefa).filter_by(id = id).first()
    return tarefa.usuario_id

def formatar_prazo(data_prazo: str, horario_prazo: str) -> Optional[datetime]:
    data_hora_prazo = datetime.strptime(f'{data_prazo} {horario_prazo}', '%d/%m/%Y %H:%M')
    return data_hora_prazo
    
