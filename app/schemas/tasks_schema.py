from pydantic import BaseModel, Field
from datetime import date


class TaskRequest(BaseModel):
    description: str
    date_to_do: date
    user_id: int | None = Field(default=None)
    created_on: date | None = Field(default=None)


class TaskResponde(TaskRequest):
    task_id: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    task_id: int | None = Field(default=None)
    user_id: int | None = Field(default=None)
    description: str | None = Field(default=None)
    created_on: date | None = Field(default=None)
    date_to_do: date | None = Field(default=None)

class ReturnPatch(BaseModel):
    message: str