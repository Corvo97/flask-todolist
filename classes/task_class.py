# -- INTERNO --
from session.base import b
# -- EXTERNO --
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


class Task(b):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    description = Column(String, nullable = False)
    created_at = Column(DateTime, default = datetime.now)
    due = Column(DateTime, nullable = False)
    completed = Column(Boolean, default = False)

    # estrangeira
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relacionamento com "User"
    user = relationship('User', back_populates = 'tasks')

    def __repr__(self):
        return f'<Task(id = {self.id}, title = {self.title}, description = {self.description}, createdat = {self.created_at}, due = {self.due}, completed = {self.completed})>'

