from typing import Annotated
from fastapi import APIRouter, HTTPException, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_204_NO_CONTENT
from ..schemas.users_schema import UserRequest, UserResponde, UserUpdate
from ..services.users_service import UsersService
from app.config.dbconfig import get_db
from sqlalchemy.orm import Session
from ..utils.current_user import get_current_user
from ..models.user_model import Users

users = APIRouter(prefix="/users", tags=["Users"])

@users.get("/", status_code=HTTP_200_OK, response_model=list[UserResponde])
def get_users(current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    """Obtener la lista de ususarios"""
    user_service = UsersService(db=db)
    return user_service.get_users()

@users.get("/{user_id}", status_code=HTTP_200_OK, response_model=UserResponde)
def get_user_by_id(user_id: int, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    """Obetener usuario por id"""
    user_service = UsersService(db=db)
    return user_service.get_user_by_id(user_id=user_id)

@users.post("/", status_code=HTTP_201_CREATED)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user_service = UsersService(db=db)
    user_service.create_user(user)
    return Response(status_code=HTTP_201_CREATED)

@users.patch("/{user_id}", status_code=HTTP_200_OK)
def update_user(user_id: int, user_update: UserUpdate, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    user_service = UsersService(db=db)
    response = user_service.update_user(user_id=user_id, user_update=user_update)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=HTTP_200_OK)

@users.delete("/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: Annotated[Users, Depends(get_current_user)], db: Session = Depends(get_db)):
    user_service = UsersService(db=db)
    response = user_service.delete_user(user_id=user_id)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
