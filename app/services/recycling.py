from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.recycling import (
    TipoResiduoRepository, PontoColetaRepository,
    PedidoDoacaoRepository, LancamentoResiduoRepository
)
from app.schemas.recycling import (
    TipoResiduo, TipoResiduoCreate, TipoResiduoUpdate,
    PontoColeta, PontoColetaCreate, PontoColetaUpdate,
    PedidoDoacao, PedidoDoacaoCreate, PedidoDoacaoUpdate,
    LancamentoResiduo, LancamentoResiduoCreate, LancamentoResiduoUpdate
)


class TipoResiduoService:
    def __init__(self, db: AsyncSession):
        self.repository = TipoResiduoRepository(db)
    
    async def get_all_tipos_residuo(self) -> List[TipoResiduo]:
        tipos = await self.repository.get_all()
        return [TipoResiduo.from_orm(t) for t in tipos]
    
    async def get_tipo_residuo_by_id(self, tipo_id: int) -> Optional[TipoResiduo]:
        tipo = await self.repository.get_by_id(tipo_id)
        return TipoResiduo.from_orm(tipo) if tipo else None
    
    async def create_tipo_residuo(self, tipo_data: TipoResiduoCreate) -> TipoResiduo:
        tipo = await self.repository.create(tipo_data)
        return TipoResiduo.from_orm(tipo)
    
    async def update_tipo_residuo(self, tipo_id: int, tipo_data: TipoResiduoUpdate) -> Optional[TipoResiduo]:
        tipo = await self.repository.update(tipo_id, tipo_data)
        return TipoResiduo.from_orm(tipo) if tipo else None
    
    async def delete_tipo_residuo(self, tipo_id: int) -> bool:
        return await self.repository.delete(tipo_id)


class PontoColetaService:
    def __init__(self, db: AsyncSession):
        self.repository = PontoColetaRepository(db)
    
    async def get_all_pontos_coleta(self) -> List[PontoColeta]:
        pontos = await self.repository.get_all()
        return [PontoColeta.from_orm(p) for p in pontos]
    
    async def get_ponto_coleta_by_id(self, ponto_id: int) -> Optional[PontoColeta]:
        ponto = await self.repository.get_by_id(ponto_id)
        return PontoColeta.from_orm(ponto) if ponto else None
    
    async def create_ponto_coleta(self, ponto_data: PontoColetaCreate) -> PontoColeta:
        ponto = await self.repository.create(ponto_data)
        return PontoColeta.from_orm(ponto)
    
    async def update_ponto_coleta(self, ponto_id: int, ponto_data: PontoColetaUpdate) -> Optional[PontoColeta]:
        ponto = await self.repository.update(ponto_id, ponto_data)
        return PontoColeta.from_orm(ponto) if ponto else None
    
    async def delete_ponto_coleta(self, ponto_id: int) -> bool:
        return await self.repository.delete(ponto_id)


class PedidoDoacaoService:
    def __init__(self, db: AsyncSession):
        self.repository = PedidoDoacaoRepository(db)
    
    async def get_all_pedidos_doacao(self) -> List[PedidoDoacao]:
        pedidos = await self.repository.get_all()
        return [PedidoDoacao.from_orm(p) for p in pedidos]
    
    async def get_pedido_doacao_by_id(self, pedido_id: int) -> Optional[PedidoDoacao]:
        pedido = await self.repository.get_by_id(pedido_id)
        return PedidoDoacao.from_orm(pedido) if pedido else None
    
    async def create_pedido_doacao(self, pedido_data: PedidoDoacaoCreate, criado_por_id: int) -> PedidoDoacao:
        pedido = await self.repository.create(pedido_data, criado_por_id)
        return PedidoDoacao.from_orm(pedido)
    
    async def update_pedido_doacao(self, pedido_id: int, pedido_data: PedidoDoacaoUpdate) -> Optional[PedidoDoacao]:
        pedido = await self.repository.update(pedido_id, pedido_data)
        return PedidoDoacao.from_orm(pedido) if pedido else None
    
    async def delete_pedido_doacao(self, pedido_id: int) -> bool:
        return await self.repository.delete(pedido_id)


class LancamentoResiduoService:
    def __init__(self, db: AsyncSession):
        self.repository = LancamentoResiduoRepository(db)
    
    async def get_all_lancamentos_residuo(self) -> List[LancamentoResiduo]:
        lancamentos = await self.repository.get_all()
        return [LancamentoResiduo.from_orm(lancamento) for lancamento in lancamentos]
    
    async def get_lancamento_residuo_by_id(self, lancamento_id: int) -> Optional[LancamentoResiduo]:
        lancamento = await self.repository.get_by_id(lancamento_id)
        return LancamentoResiduo.from_orm(lancamento) if lancamento else None
    
    async def create_lancamento_residuo(self, lancamento_data: LancamentoResiduoCreate) -> LancamentoResiduo:
        lancamento = await self.repository.create(lancamento_data)
        return LancamentoResiduo.from_orm(lancamento)
    
    async def update_lancamento_residuo(self, lancamento_id: int, lancamento_data: LancamentoResiduoUpdate) -> Optional[LancamentoResiduo]:
        lancamento = await self.repository.update(lancamento_id, lancamento_data)
        return LancamentoResiduo.from_orm(lancamento) if lancamento else None
    
    async def delete_lancamento_residuo(self, lancamento_id: int) -> bool:
        return await self.repository.delete(lancamento_id)
