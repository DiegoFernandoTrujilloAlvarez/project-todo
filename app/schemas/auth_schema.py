from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponde(BaseModel):
    token: str
    token_type:str
