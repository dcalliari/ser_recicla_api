from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.recycling import (
    TipoResiduoService, PontoColetaService,
    PedidoDoacaoService, LancamentoResiduoService
)
from app.schemas.recycling import (
    TipoResiduo, TipoResiduoCreate,
    PontoColeta, PontoColetaCreate, PontoColetaUpdate,
    PedidoDoacao, PedidoDoacaoCreate, PedidoDoacaoUpdate,
    LancamentoResiduo, LancamentoResiduoCreate, LancamentoResiduoUpdate
)
from app.deps import get_current_active_user, require_perfil
from app.db.models.user import User

router = APIRouter()


# Tipo Resíduo endpoints
@router.get("/tipo-residuo/", response_model=List[TipoResiduo])
async def get_tipos_residuo(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = TipoResiduoService(db)
    return await service.get_all_tipos_residuo()


@router.post("/tipo-residuo/", response_model=TipoResiduo)
async def create_tipo_residuo(
    tipo_data: TipoResiduoCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    service = TipoResiduoService(db)
    return await service.create_tipo_residuo(tipo_data)


# Ponto Coleta endpoints
@router.get("/pontos-coleta/", response_model=List[PontoColeta])
async def get_pontos_coleta(
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = PontoColetaService(db)
    return await service.get_all_pontos_coleta()


@router.post("/pontos-coleta/", response_model=PontoColeta)
async def create_ponto_coleta(
    ponto_data: PontoColetaCreate,
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = PontoColetaService(db)
    return await service.create_ponto_coleta(ponto_data)


@router.get("/ponto-coleta/{ponto_id}/", response_model=PontoColeta)
async def get_ponto_coleta(
    ponto_id: int,
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = PontoColetaService(db)
    ponto = await service.get_ponto_coleta_by_id(ponto_id)
    
    if not ponto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto não encontrado"
        )
    
    return ponto


@router.put("/ponto-coleta/{ponto_id}/", response_model=PontoColeta)
async def update_ponto_coleta(
    ponto_id: int,
    ponto_data: PontoColetaUpdate,
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = PontoColetaService(db)
    ponto = await service.update_ponto_coleta(ponto_id, ponto_data)
    
    if not ponto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto de coleta não encontrado."
        )
    
    return ponto


@router.delete("/ponto-coleta/{ponto_id}/")
async def delete_ponto_coleta(
    ponto_id: int,
    current_user: User = Depends(require_perfil("ADMIN_UNI")),
    db: AsyncSession = Depends(get_db)
):
    service = PontoColetaService(db)
    deleted = await service.delete_ponto_coleta(ponto_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto de coleta não encontrado."
        )
    
    return {"detail": "Ponto de coleta deletado com sucesso"}


# Pedido Doação endpoints
@router.get("/pedido-doacao/", response_model=List[PedidoDoacao])
async def get_pedidos_doacao(
    current_user: User = Depends(require_perfil("CHEFE")),
    db: AsyncSession = Depends(get_db)
):
    service = PedidoDoacaoService(db)
    return await service.get_all_pedidos_doacao()


@router.post("/pedido-doacao/", response_model=PedidoDoacao)
async def create_pedido_doacao(
    pedido_data: PedidoDoacaoCreate,
    current_user: User = Depends(require_perfil("CHEFE")),
    db: AsyncSession = Depends(get_db)
):
    service = PedidoDoacaoService(db)
    return await service.create_pedido_doacao(pedido_data, current_user.id)


@router.get("/pedido-doacao/{pedido_id}/", response_model=PedidoDoacao)
async def get_pedido_doacao(
    pedido_id: int,
    current_user: User = Depends(require_perfil("CHEFE")),
    db: AsyncSession = Depends(get_db)
):
    service = PedidoDoacaoService(db)
    pedido = await service.get_pedido_doacao_by_id(pedido_id)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    return pedido


@router.put("/pedido-doacao/{pedido_id}/", response_model=PedidoDoacao)
async def update_pedido_doacao(
    pedido_id: int,
    pedido_data: PedidoDoacaoUpdate,
    current_user: User = Depends(require_perfil("CHEFE")),
    db: AsyncSession = Depends(get_db)
):
    service = PedidoDoacaoService(db)
    pedido = await service.update_pedido_doacao(pedido_id, pedido_data)
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    return pedido


@router.delete("/pedido-doacao/{pedido_id}/")
async def delete_pedido_doacao(
    pedido_id: int,
    current_user: User = Depends(require_perfil("CHEFE")),
    db: AsyncSession = Depends(get_db)
):
    service = PedidoDoacaoService(db)
    deleted = await service.delete_pedido_doacao(pedido_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    return {"detail": "Pedido deletado com sucesso"}


# Lançamento Resíduo endpoints
@router.get("/lancamento-residuo/", response_model=List[LancamentoResiduo])
async def get_lancamentos_residuo(
    current_user: User = Depends(require_perfil("PONTO")),
    db: AsyncSession = Depends(get_db)
):
    service = LancamentoResiduoService(db)
    return await service.get_all_lancamentos_residuo()


@router.post("/lancamento-residuo/", response_model=LancamentoResiduo)
async def create_lancamento_residuo(
    lancamento_data: LancamentoResiduoCreate,
    current_user: User = Depends(require_perfil("PONTO")),
    db: AsyncSession = Depends(get_db)
):
    service = LancamentoResiduoService(db)
    return await service.create_lancamento_residuo(lancamento_data)


@router.get("/lancamento-residuo/{lancamento_id}/", response_model=LancamentoResiduo)
async def get_lancamento_residuo(
    lancamento_id: int,
    current_user: User = Depends(require_perfil("PONTO")),
    db: AsyncSession = Depends(get_db)
):
    service = LancamentoResiduoService(db)
    lancamento = await service.get_lancamento_residuo_by_id(lancamento_id)
    
    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    return lancamento


@router.put("/lancamento-residuo/{lancamento_id}/", response_model=LancamentoResiduo)
async def update_lancamento_residuo(
    lancamento_id: int,
    lancamento_data: LancamentoResiduoUpdate,
    current_user: User = Depends(require_perfil("PONTO")),
    db: AsyncSession = Depends(get_db)
):
    service = LancamentoResiduoService(db)
    lancamento = await service.update_lancamento_residuo(lancamento_id, lancamento_data)
    
    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    return lancamento


@router.delete("/lancamento-residuo/{lancamento_id}/")
async def delete_lancamento_residuo(
    lancamento_id: int,
    current_user: User = Depends(require_perfil("PONTO")),
    db: AsyncSession = Depends(get_db)
):
    service = LancamentoResiduoService(db)
    deleted = await service.delete_lancamento_residuo(lancamento_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    return {"detail": "Lançamento deletado com sucesso"}
