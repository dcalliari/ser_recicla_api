from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.institutional import UniversidadeService, UnidadeService, CursoService, TurmaService
from app.schemas.institutional import (
    Universidade, UniversidadeCreate,
    Unidade, UnidadeCreate,
    Curso, CursoCreate,
    Turma, TurmaCreate
)
from app.deps import get_current_active_user, require_perfil
from app.db.models.user import User

router = APIRouter()


@router.get("/university/", response_model=List[Universidade])
async def get_universidades(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = UniversidadeService(db)
    return await service.get_all_universidades()


@router.post("/university/", response_model=Universidade)
async def create_universidade(
    universidade_data: UniversidadeCreate,
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = UniversidadeService(db)
    return await service.create_universidade(universidade_data)


@router.get("/unit/", response_model=List[Unidade])
async def get_unidades(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = UnidadeService(db)
    return await service.get_all_unidades()


@router.post("/unit/", response_model=Unidade)
async def create_unidade(
    unidade_data: UnidadeCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = UnidadeService(db)
    return await service.create_unidade(unidade_data)


@router.get("/course/", response_model=List[Curso])
async def get_cursos(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CursoService(db)
    return await service.get_all_cursos()


@router.post("/course/", response_model=Curso)
async def create_curso(
    curso_data: CursoCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = CursoService(db)
    return await service.create_curso(curso_data)


@router.get("/class/", response_model=List[Turma])
async def get_turmas(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = TurmaService(db)
    return await service.get_all_turmas()


@router.post("/class/", response_model=Turma)
async def create_turma(
    turma_data: TurmaCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = TurmaService(db)
    return await service.create_turma(turma_data)
