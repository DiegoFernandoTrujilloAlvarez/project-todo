from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..config.dbconfig import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    firt_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    email = Column(String(100), index=True, unique=True)
    password = Column(String(2000), default=None)

    # Relación con TASK
    tasks = relationship("Tasks", back_populates="owner")

    