from sqlalchemy.orm import Session


class BaseService():
    def __init__(self, db: Session):
        """Inicializar la sesión de base de datos"""
        self.db = db
    