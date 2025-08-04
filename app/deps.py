from typing import Annotated
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import User
from app.core.security import verify_token
from app.schemas.user import TokenData

security = HTTPBearer()


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    try:
        payload = verify_token(credentials.credentials, "access")
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


def require_perfil(perfil: str):
    def perfil_dependency(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ):
        if current_user.perfil != perfil:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return perfil_dependency


# Dependências específicas para cada perfil
AdminUniversidade = Depends(require_perfil("ADMIN_UNI"))
Coordenador = Depends(require_perfil("COORD"))
ChefeTurma = Depends(require_perfil("CHEFE"))  
PontoColeta = Depends(require_perfil("PONTO"))
Aluno = Depends(require_perfil("ALUNO"))


def get_refresh_token_from_cookie(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token not found"
        )
    return refresh_token
