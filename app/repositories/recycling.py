from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.recycling import TipoResiduo, PontoColeta, PedidoDoacao, LancamentoResiduo
from app.db.models.user import User
from app.schemas.recycling import (
    TipoResiduoCreate, TipoResiduoUpdate,
    PontoColetaCreate, PontoColetaUpdate,
    PedidoDoacaoCreate, PedidoDoacaoUpdate,
    LancamentoResiduoCreate, LancamentoResiduoUpdate
)


class TipoResiduoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[TipoResiduo]:
        result = await self.db.execute(select(TipoResiduo))
        return result.scalars().all()
    
    async def get_by_id(self, tipo_id: int) -> Optional[TipoResiduo]:
        result = await self.db.execute(select(TipoResiduo).where(TipoResiduo.id == tipo_id))
        return result.scalar_one_or_none()
    
    async def create(self, tipo_data: TipoResiduoCreate) -> TipoResiduo:
        tipo = TipoResiduo(**tipo_data.dict())
        self.db.add(tipo)
        await self.db.commit()
        await self.db.refresh(tipo)
        return tipo
    
    async def update(self, tipo_id: int, tipo_data: TipoResiduoUpdate) -> Optional[TipoResiduo]:
        tipo = await self.get_by_id(tipo_id)
        if not tipo:
            return None
        
        update_data = tipo_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tipo, field, value)
        
        await self.db.commit()
        await self.db.refresh(tipo)
        return tipo
    
    async def delete(self, tipo_id: int) -> bool:
        tipo = await self.get_by_id(tipo_id)
        if not tipo:
            return False
        
        await self.db.delete(tipo)
        await self.db.commit()
        return True


class PontoColetaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[PontoColeta]:
        result = await self.db.execute(
            select(PontoColeta).options(
                selectinload(PontoColeta.universidade),
                selectinload(PontoColeta.unidade),
                selectinload(PontoColeta.responsavel)
            )
        )
        return result.scalars().all()
    
    async def get_by_id(self, ponto_id: int) -> Optional[PontoColeta]:
        result = await self.db.execute(
            select(PontoColeta).options(
                selectinload(PontoColeta.universidade),
                selectinload(PontoColeta.unidade),
                selectinload(PontoColeta.responsavel)
            ).where(PontoColeta.id == ponto_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, ponto_data: PontoColetaCreate) -> PontoColeta:
        ponto = PontoColeta(**ponto_data.dict())
        self.db.add(ponto)
        await self.db.commit()
        await self.db.refresh(ponto)
        return ponto
    
    async def update(self, ponto_id: int, ponto_data: PontoColetaUpdate) -> Optional[PontoColeta]:
        ponto = await self.get_by_id(ponto_id)
        if not ponto:
            return None
        
        update_data = ponto_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(ponto, field, value)
        
        await self.db.commit()
        await self.db.refresh(ponto)
        return ponto
    
    async def delete(self, ponto_id: int) -> bool:
        ponto = await self.get_by_id(ponto_id)
        if not ponto:
            return False
        
        await self.db.delete(ponto)
        await self.db.commit()
        return True


class PedidoDoacaoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[PedidoDoacao]:
        result = await self.db.execute(
            select(PedidoDoacao).options(
                selectinload(PedidoDoacao.criado_por),
                selectinload(PedidoDoacao.turma),
                selectinload(PedidoDoacao.alunos)
            )
        )
        return result.scalars().all()
    
    async def get_by_id(self, pedido_id: int) -> Optional[PedidoDoacao]:
        result = await self.db.execute(
            select(PedidoDoacao).options(
                selectinload(PedidoDoacao.criado_por),
                selectinload(PedidoDoacao.turma),
                selectinload(PedidoDoacao.alunos)
            ).where(PedidoDoacao.id == pedido_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, pedido_data: PedidoDoacaoCreate, criado_por_id: int) -> PedidoDoacao:
        # Buscar alunos
        alunos = []
        if pedido_data.alunos:
            result = await self.db.execute(
                select(User).where(User.id.in_(pedido_data.alunos))
            )
            alunos = result.scalars().all()
        
        pedido_dict = pedido_data.dict(exclude={"alunos"})
        pedido_dict["criado_por_id"] = criado_por_id
        
        pedido = PedidoDoacao(**pedido_dict)
        pedido.alunos = alunos
        
        self.db.add(pedido)
        await self.db.commit()
        await self.db.refresh(pedido)
        return pedido
    
    async def update(self, pedido_id: int, pedido_data: PedidoDoacaoUpdate) -> Optional[PedidoDoacao]:
        pedido = await self.get_by_id(pedido_id)
        if not pedido:
            return None
        
        update_data = pedido_data.dict(exclude_unset=True, exclude={"alunos"})
        for field, value in update_data.items():
            setattr(pedido, field, value)
        
        # Atualizar alunos se fornecido
        if pedido_data.alunos is not None:
            result = await self.db.execute(
                select(User).where(User.id.in_(pedido_data.alunos))
            )
            pedido.alunos = result.scalars().all()
        
        await self.db.commit()
        await self.db.refresh(pedido)
        return pedido
    
    async def delete(self, pedido_id: int) -> bool:
        pedido = await self.get_by_id(pedido_id)
        if not pedido:
            return False
        
        await self.db.delete(pedido)
        await self.db.commit()
        return True


class LancamentoResiduoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> List[LancamentoResiduo]:
        result = await self.db.execute(
            select(LancamentoResiduo).options(
                selectinload(LancamentoResiduo.pedido),
                selectinload(LancamentoResiduo.ponto_coleta),
                selectinload(LancamentoResiduo.tipo_residuo)
            )
        )
        return result.scalars().all()
    
    async def get_by_id(self, lancamento_id: int) -> Optional[LancamentoResiduo]:
        result = await self.db.execute(
            select(LancamentoResiduo).options(
                selectinload(LancamentoResiduo.pedido),
                selectinload(LancamentoResiduo.ponto_coleta),
                selectinload(LancamentoResiduo.tipo_residuo)
            ).where(LancamentoResiduo.id == lancamento_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, lancamento_data: LancamentoResiduoCreate) -> LancamentoResiduo:
        lancamento = LancamentoResiduo(**lancamento_data.dict())
        self.db.add(lancamento)
        await self.db.commit()
        await self.db.refresh(lancamento)
        return lancamento
    
    async def update(self, lancamento_id: int, lancamento_data: LancamentoResiduoUpdate) -> Optional[LancamentoResiduo]:
        lancamento = await self.get_by_id(lancamento_id)
        if not lancamento:
            return None
        
        update_data = lancamento_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lancamento, field, value)
        
        await self.db.commit()
        await self.db.refresh(lancamento)
        return lancamento
    
    async def delete(self, lancamento_id: int) -> bool:
        lancamento = await self.get_by_id(lancamento_id)
        if not lancamento:
            return False
        
        await self.db.delete(lancamento)
        await self.db.commit()
        return True
