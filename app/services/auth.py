from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import User, UserCreate, UserUpdate, UserInfo, Token
from app.core.security import create_access_token, create_refresh_token, verify_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.authenticate(username, password)
        return User.from_orm(user) if user else None
    
    async def create_tokens(self, user: User) -> Token:
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        try:
            payload = verify_token(refresh_token, "refresh")
            user_id = payload.get("user_id")
            username = payload.get("sub")
            
            if not user_id or not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            # Verificar se o usuário ainda existe
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            access_token = create_access_token(data={"sub": username, "user_id": user_id})
            new_refresh_token = create_refresh_token(data={"sub": username, "user_id": user_id})
            
            return {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    
    async def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        role_mapping = {
            'ADMIN_UNI': 'administrador',
            'COORD': 'coordenador',
            'CHEFE': 'chefe_turma',
            'ALUNO': 'aluno',
            'PONTO': 'ponto_coleta',
        }
        
        return UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            role=role_mapping.get(user.perfil, 'desconhecido'),
            universidade=user.universidade.nome if user.universidade else None,
            unidade=user.unidade.nome if user.unidade else None,
            turma=user.turma.nome if user.turma else None
        )


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    async def create_user(self, user_data: UserCreate, perfil: str) -> User:
        # Verificar se username já existe
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Verificar se email já existe
        existing_email = await self.repository.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = await self.repository.create(user_data, perfil)
        return User.from_orm(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = await self.repository.get_by_id(user_id)
        return User.from_orm(user) if user else None
    
    async def get_all_users(self) -> List[User]:
        users = await self.repository.get_all()
        return [User.from_orm(u) for u in users]
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.repository.update(user_id, user_data)
        return User.from_orm(user) if user else None
    
    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)
