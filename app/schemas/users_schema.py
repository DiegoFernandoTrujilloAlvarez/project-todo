from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    firt_name: str
    last_name: str
    email: str


class UserResponde(UserRequest):
    user_id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    user_id: int | None = Field(default=None)
    firt_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str | None = Field(default=None)

class ReturnPatch(BaseModel):
    message: str