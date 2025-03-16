from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_204_NO_CONTENT
from ..schemas.auth_schema import AuthRequest, AuthResponde
from ..services.auth_service import AuthService
from app.config.dbconfig import get_db
from sqlalchemy.orm import Session
from typing import Annotated

oauth = APIRouter(prefix="/oauth", tags=["Auth"])


@oauth.post("/token", status_code=HTTP_200_OK, response_model=AuthResponde)
async def login_for_access_token(auth: AuthRequest, db: Session = Depends(get_db)):
    authService = AuthService(db=db)
    response = authService.get_token(auth=auth)
    return response