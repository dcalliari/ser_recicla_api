from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.auth import AuthService, UserService
from app.schemas.user import User, UserCreate, UserInfo
from app.deps import get_current_active_user, get_refresh_token_from_cookie, require_perfil
from app.core.config import settings

router = APIRouter()


@router.post("/login/", response_model=dict)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    tokens = await auth_service.create_tokens(user)
    
    # Definir cookie do refresh token
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=False,  # Definir True em produção com HTTPS
        samesite="lax"
    )
    
    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"],
        "username": user.username
    }


@router.post("/refresh/", response_model=dict)
async def refresh_token(
    response: Response,
    refresh_token: str = Depends(get_refresh_token_from_cookie),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    tokens = await auth_service.refresh_access_token(refresh_token)
    
    # Definir novo cookie do refresh token
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=False,  # Definir True em produção com HTTPS
        samesite="lax"
    )
    
    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"]
    }


@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"detail": "Successfully logged out"}


@router.get("/me/", response_model=UserInfo)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user_info = await auth_service.get_user_info(current_user.id)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_info


@router.post("/signup/coord/", response_model=User)
async def create_coordenador(
    user_data: UserCreate,
    current_user: Annotated[User, Depends(require_perfil("ADMIN_UNI"))],
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.create_user(user_data, "COORD")


@router.post("/signup/ponto/", response_model=User)
async def create_ponto_coleta(
    user_data: UserCreate,
    current_user: Annotated[User, Depends(require_perfil("ADMIN_UNI"))],
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.create_user(user_data, "PONTO")


@router.post("/signup/chefe/", response_model=User)
async def create_chefe_turma(
    user_data: UserCreate,
    current_user: Annotated[User, Depends(require_perfil("COORD"))],
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.create_user(user_data, "CHEFE")


@router.post("/signup/aluno/", response_model=User)
async def create_aluno(
    user_data: UserCreate,
    current_user: Annotated[User, Depends(require_perfil("CHEFE"))],
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.create_user(user_data, "ALUNO")
