from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[User]:
        result = await self.db.execute(
            select(User).options(
                selectinload(User.universidade),
                selectinload(User.unidade),
                selectinload(User.turma)
            )
        )
        return result.scalars().all()
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).options(
                selectinload(User.universidade),
                selectinload(User.unidade),
                selectinload(User.turma)
            ).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).options(
                selectinload(User.universidade),
                selectinload(User.unidade),
                selectinload(User.turma)
            ).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create(self, user_data: UserCreate, perfil: str) -> User:
        user_dict = user_data.dict(exclude={"password"})
        user_dict["perfil"] = perfil
        user_dict["hashed_password"] = get_password_hash(user_data.password)
        
        user = User(**user_dict)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        return True
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        from app.core.security import verify_password
        
        user = await self.get_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
