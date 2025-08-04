from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.institutional import (
    UniversidadeRepository, UnidadeRepository, 
    CursoRepository, TurmaRepository
)
from app.schemas.institutional import (
    Universidade, UniversidadeCreate, UniversidadeUpdate,
    Unidade, UnidadeCreate, UnidadeUpdate,
    Curso, CursoCreate, CursoUpdate,
    Turma, TurmaCreate, TurmaUpdate
)


class UniversidadeService:
    def __init__(self, db: AsyncSession):
        self.repository = UniversidadeRepository(db)
    
    async def get_all_universidades(self) -> List[Universidade]:
        universidades = await self.repository.get_all()
        return [Universidade.from_orm(u) for u in universidades]
    
    async def get_universidade_by_id(self, universidade_id: int) -> Optional[Universidade]:
        universidade = await self.repository.get_by_id(universidade_id)
        return Universidade.from_orm(universidade) if universidade else None
    
    async def create_universidade(self, universidade_data: UniversidadeCreate) -> Universidade:
        universidade = await self.repository.create(universidade_data)
        return Universidade.from_orm(universidade)
    
    async def update_universidade(self, universidade_id: int, universidade_data: UniversidadeUpdate) -> Optional[Universidade]:
        universidade = await self.repository.update(universidade_id, universidade_data)
        return Universidade.from_orm(universidade) if universidade else None
    
    async def delete_universidade(self, universidade_id: int) -> bool:
        return await self.repository.delete(universidade_id)


class UnidadeService:
    def __init__(self, db: AsyncSession):
        self.repository = UnidadeRepository(db)
    
    async def get_all_unidades(self) -> List[Unidade]:
        unidades = await self.repository.get_all()
        return [Unidade.from_orm(u) for u in unidades]
    
    async def get_unidade_by_id(self, unidade_id: int) -> Optional[Unidade]:
        unidade = await self.repository.get_by_id(unidade_id)
        return Unidade.from_orm(unidade) if unidade else None
    
    async def create_unidade(self, unidade_data: UnidadeCreate) -> Unidade:
        unidade = await self.repository.create(unidade_data)
        return Unidade.from_orm(unidade)
    
    async def update_unidade(self, unidade_id: int, unidade_data: UnidadeUpdate) -> Optional[Unidade]:
        unidade = await self.repository.update(unidade_id, unidade_data)
        return Unidade.from_orm(unidade) if unidade else None
    
    async def delete_unidade(self, unidade_id: int) -> bool:
        return await self.repository.delete(unidade_id)


class CursoService:
    def __init__(self, db: AsyncSession):
        self.repository = CursoRepository(db)
    
    async def get_all_cursos(self) -> List[Curso]:
        cursos = await self.repository.get_all()
        return [Curso.from_orm(c) for c in cursos]
    
    async def get_curso_by_id(self, curso_id: int) -> Optional[Curso]:
        curso = await self.repository.get_by_id(curso_id)
        return Curso.from_orm(curso) if curso else None
    
    async def create_curso(self, curso_data: CursoCreate) -> Curso:
        curso = await self.repository.create(curso_data)
        return Curso.from_orm(curso)
    
    async def update_curso(self, curso_id: int, curso_data: CursoUpdate) -> Optional[Curso]:
        curso = await self.repository.update(curso_id, curso_data)
        return Curso.from_orm(curso) if curso else None
    
    async def delete_curso(self, curso_id: int) -> bool:
        return await self.repository.delete(curso_id)


class TurmaService:
    def __init__(self, db: AsyncSession):
        self.repository = TurmaRepository(db)
    
    async def get_all_turmas(self) -> List[Turma]:
        turmas = await self.repository.get_all()
        return [Turma.from_orm(t) for t in turmas]
    
    async def get_turma_by_id(self, turma_id: int) -> Optional[Turma]:
        turma = await self.repository.get_by_id(turma_id)
        return Turma.from_orm(turma) if turma else None
    
    async def create_turma(self, turma_data: TurmaCreate) -> Turma:
        turma = await self.repository.create(turma_data)
        return Turma.from_orm(turma)
    
    async def update_turma(self, turma_id: int, turma_data: TurmaUpdate) -> Optional[Turma]:
        turma = await self.repository.update(turma_id, turma_data)
        return Turma.from_orm(turma) if turma else None
    
    async def delete_turma(self, turma_id: int) -> bool:
        return await self.repository.delete(turma_id)
