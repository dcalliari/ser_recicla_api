from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    perfil: str
    universidade_id: Optional[int] = None
    unidade_id: Optional[int] = None
    turma_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    perfil: Optional[str] = None
    universidade_id: Optional[int] = None
    unidade_id: Optional[int] = None
    turma_id: Optional[int] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    date_joined: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    role: str
    universidade: Optional[str] = None
    unidade: Optional[str] = None
    turma: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
