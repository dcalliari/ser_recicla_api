from pydantic import BaseModel
from typing import Optional


class UniversidadeBase(BaseModel):
    nome: str


class UniversidadeCreate(UniversidadeBase):
    pass


class UniversidadeUpdate(BaseModel):
    nome: Optional[str] = None


class Universidade(UniversidadeBase):
    id: int

    class Config:
        from_attributes = True


class UnidadeBase(BaseModel):
    nome: str
    universidade_id: int


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeUpdate(BaseModel):
    nome: Optional[str] = None
    universidade_id: Optional[int] = None


class Unidade(UnidadeBase):
    id: int

    class Config:
        from_attributes = True


class CursoBase(BaseModel):
    nome: str
    universidade_id: int
    unidade_id: int


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nome: Optional[str] = None
    universidade_id: Optional[int] = None
    unidade_id: Optional[int] = None


class Curso(CursoBase):
    id: int

    class Config:
        from_attributes = True


class TurmaBase(BaseModel):
    nome: str
    curso_id: int
    unidade_id: int
    universidade_id: int


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    curso_id: Optional[int] = None
    unidade_id: Optional[int] = None
    universidade_id: Optional[int] = None


class Turma(TurmaBase):
    id: int

    class Config:
        from_attributes = True
