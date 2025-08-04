from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class TipoResiduoBase(BaseModel):
    nome: str


class TipoResiduoCreate(TipoResiduoBase):
    pass


class TipoResiduoUpdate(BaseModel):
    nome: Optional[str] = None


class TipoResiduo(TipoResiduoBase):
    id: int

    class Config:
        from_attributes = True


class PontoColetaBase(BaseModel):
    nome: str
    universidade_id: int
    unidade_id: int
    responsavel_id: Optional[int] = None


class PontoColetaCreate(PontoColetaBase):
    pass


class PontoColetaUpdate(BaseModel):
    nome: Optional[str] = None
    universidade_id: Optional[int] = None
    unidade_id: Optional[int] = None
    responsavel_id: Optional[int] = None


class PontoColeta(PontoColetaBase):
    id: int

    class Config:
        from_attributes = True


class PedidoDoacaoBase(BaseModel):
    codigo: str
    turma_id: int
    alunos: List[int] = []


class PedidoDoacaoCreate(PedidoDoacaoBase):
    pass


class PedidoDoacaoUpdate(BaseModel):
    codigo: Optional[str] = None
    turma_id: Optional[int] = None
    alunos: Optional[List[int]] = None
    confirmado: Optional[bool] = None


class PedidoDoacao(PedidoDoacaoBase):
    id: int
    criado_por_id: Optional[int] = None
    criado_em: datetime
    confirmado: bool

    class Config:
        from_attributes = True


class LancamentoResiduoBase(BaseModel):
    pedido_id: int
    ponto_coleta_id: int
    tipo_residuo_id: int
    peso_kg: Decimal


class LancamentoResiduoCreate(LancamentoResiduoBase):
    pass


class LancamentoResiduoUpdate(BaseModel):
    pedido_id: Optional[int] = None
    ponto_coleta_id: Optional[int] = None
    tipo_residuo_id: Optional[int] = None
    peso_kg: Optional[Decimal] = None


class LancamentoResiduo(LancamentoResiduoBase):
    id: int
    data: datetime

    class Config:
        from_attributes = True
