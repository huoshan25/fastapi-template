from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.modules.user.models import User


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode: True


class UserLogin(BaseModel):
    username: str
    password: str


UserInDB = pydantic_model_creator(User, name="UserInDB", exclude=("password",))