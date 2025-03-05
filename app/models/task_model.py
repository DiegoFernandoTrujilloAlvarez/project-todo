from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..config.dbconfig import Base


class Tasks(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    created_on = Column(Date, nullable=False)
    date_to_do = Column(Date, nullable=False)

    # Relación inversa
    owner = relationship("Users", back_populates="tasks")