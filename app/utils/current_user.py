from ..services.users_service import UsersService
from fastapi import HTTPException, status, Depends, Header
from app.config.authconfig import SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from app.config.dbconfig import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token")
bearer_scheme = HTTPBearer()


async def get_current_user(authentication: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(authentication.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    userService = UsersService(db=db)
    user = userService.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user