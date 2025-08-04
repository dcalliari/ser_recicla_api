from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.institutional import Universidade, Unidade, Curso, Turma
from app.schemas.institutional import (
    UniversidadeCreate, UniversidadeUpdate,
    UnidadeCreate, UnidadeUpdate,
    CursoCreate, CursoUpdate,
    TurmaCreate, TurmaUpdate
)


class UniversidadeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[Universidade]:
        result = await self.db.execute(select(Universidade))
        return result.scalars().all()
    
    async def get_by_id(self, universidade_id: int) -> Optional[Universidade]:
        result = await self.db.execute(select(Universidade).where(Universidade.id == universidade_id))
        return result.scalar_one_or_none()
    
    async def create(self, universidade_data: UniversidadeCreate) -> Universidade:
        universidade = Universidade(**universidade_data.dict())
        self.db.add(universidade)
        await self.db.commit()
        await self.db.refresh(universidade)
        return universidade
    
    async def update(self, universidade_id: int, universidade_data: UniversidadeUpdate) -> Optional[Universidade]:
        universidade = await self.get_by_id(universidade_id)
        if not universidade:
            return None
        
        update_data = universidade_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(universidade, field, value)
        
        await self.db.commit()
        await self.db.refresh(universidade)
        return universidade
    
    async def delete(self, universidade_id: int) -> bool:
        universidade = await self.get_by_id(universidade_id)
        if not universidade:
            return False
        
        await self.db.delete(universidade)
        await self.db.commit()
        return True


class UnidadeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[Unidade]:
        result = await self.db.execute(select(Unidade))
        return result.scalars().all()
    
    async def get_by_id(self, unidade_id: int) -> Optional[Unidade]:
        result = await self.db.execute(select(Unidade).where(Unidade.id == unidade_id))
        return result.scalar_one_or_none()
    
    async def create(self, unidade_data: UnidadeCreate) -> Unidade:
        unidade = Unidade(**unidade_data.dict())
        self.db.add(unidade)
        await self.db.commit()
        await self.db.refresh(unidade)
        return unidade
    
    async def update(self, unidade_id: int, unidade_data: UnidadeUpdate) -> Optional[Unidade]:
        unidade = await self.get_by_id(unidade_id)
        if not unidade:
            return None
        
        update_data = unidade_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(unidade, field, value)
        
        await self.db.commit()
        await self.db.refresh(unidade)
        return unidade
    
    async def delete(self, unidade_id: int) -> bool:
        unidade = await self.get_by_id(unidade_id)
        if not unidade:
            return False
        
        await self.db.delete(unidade)
        await self.db.commit()
        return True


class CursoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[Curso]:
        result = await self.db.execute(select(Curso))
        return result.scalars().all()
    
    async def get_by_id(self, curso_id: int) -> Optional[Curso]:
        result = await self.db.execute(select(Curso).where(Curso.id == curso_id))
        return result.scalar_one_or_none()
    
    async def create(self, curso_data: CursoCreate) -> Curso:
        curso = Curso(**curso_data.dict())
        self.db.add(curso)
        await self.db.commit()
        await self.db.refresh(curso)
        return curso
    
    async def update(self, curso_id: int, curso_data: CursoUpdate) -> Optional[Curso]:
        curso = await self.get_by_id(curso_id)
        if not curso:
            return None
        
        update_data = curso_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(curso, field, value)
        
        await self.db.commit()
        await self.db.refresh(curso)
        return curso
    
    async def delete(self, curso_id: int) -> bool:
        curso = await self.get_by_id(curso_id)
        if not curso:
            return False
        
        await self.db.delete(curso)
        await self.db.commit()
        return True


class TurmaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[Turma]:
        result = await self.db.execute(select(Turma))
        return result.scalars().all()
    
    async def get_by_id(self, turma_id: int) -> Optional[Turma]:
        result = await self.db.execute(select(Turma).where(Turma.id == turma_id))
        return result.scalar_one_or_none()
    
    async def create(self, turma_data: TurmaCreate) -> Turma:
        turma = Turma(**turma_data.dict())
        self.db.add(turma)
        await self.db.commit()
        await self.db.refresh(turma)
        return turma
    
    async def update(self, turma_id: int, turma_data: TurmaUpdate) -> Optional[Turma]:
        turma = await self.get_by_id(turma_id)
        if not turma:
            return None
        
        update_data = turma_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(turma, field, value)
        
        await self.db.commit()
        await self.db.refresh(turma)
        return turma
    
    async def delete(self, turma_id: int) -> bool:
        turma = await self.get_by_id(turma_id)
        if not turma:
            return False
        
        await self.db.delete(turma)
        await self.db.commit()
        return True
