# -- interno --
from classes.user_class import User
from classes.task_class import Task
from session.session import with_session
# -- externo --
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from flask_login import current_user
from sqlalchemy.orm import joinedload


@with_session
def get_task_owner(session: Session, id: int) -> int:
    task = session.query(Task).filter_by(id = id).first()
    return task.user_id

def format_due_date(date_due: str, time_due: str) -> Optional[datetime]:
    date_time_due = datetime.strptime(f'{date_due} {time_due}', '%d/%m/%Y %H:%M')
    return date_time_due
    
