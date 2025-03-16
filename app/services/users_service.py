from ..models.user_model import Users
from .base_service import BaseService
from ..schemas.users_schema import UserRequest, UserUpdate
from fastapi import HTTPException

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService(BaseService):

    def get_users(self):
        """Obtiene todos los usuarios"""
        return self.db.query(Users).all()
    
    def get_user_by_id(self, user_id: int):
        """Obtiene el usuario por id"""
        return self.db.query(Users).filter(Users.user_id == user_id).first()     

    def get_user_by_email(self, email: str):
        """Obtiene el usuario por email"""
        return self.db.query(Users).filter(Users.email == email).first()   

    def create_user(self, user: UserRequest):
        """Crea nuevo ususario"""
        new_user = Users(**user.model_dump())
        user_exists = self.db.query(Users).filter(Users.email == new_user.email).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="User exists")
        new_user.password = pwd_context.hash(user.password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Actualización de un usuario"""
        # Buscar usuario (Después reemplazar con la función de get ususario)
        user = self.db.query(Users).filter(Users.user_id == user_id).first()
        if not user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return True
    
    def delete_user(self, user_id: int):
        """Eliminar un usuario"""
        user = self.db.query(Users).filter(Users.user_id == user_id).first()
        if not user:
            None
        self.db.delete(user)
        return True
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email=email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user
    