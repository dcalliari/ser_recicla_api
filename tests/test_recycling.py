import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.recycling import TipoResiduoService, PontoColetaService
from app.services.institutional import UniversidadeService, UnidadeService
from app.schemas.recycling import TipoResiduoCreate, PontoColetaCreate
from app.schemas.institutional import UniversidadeCreate, UnidadeCreate


class TestRecycling:
    
    @pytest.mark.asyncio
    async def test_create_tipo_residuo(self, db_session: AsyncSession):
        """Test creating a waste type"""
        service = TipoResiduoService(db_session)
        tipo_data = TipoResiduoCreate(nome="Papel")
        
        tipo = await service.create_tipo_residuo(tipo_data)
        
        assert tipo.id is not None
        assert tipo.nome == "Papel"
    
    @pytest.mark.asyncio
    async def test_get_all_tipos_residuo(self, db_session: AsyncSession):
        """Test getting all waste types"""
        service = TipoResiduoService(db_session)
        
        # Create test data
        tipo_data = TipoResiduoCreate(nome="Plástico")
        await service.create_tipo_residuo(tipo_data)
        
        tipos = await service.get_all_tipos_residuo()
        
        assert len(tipos) >= 1
        assert any(t.nome == "Plástico" for t in tipos)
    
    @pytest.mark.asyncio
    async def test_create_ponto_coleta(self, db_session: AsyncSession):
        """Test creating a collection point"""
        # First create university and unit
        uni_service = UniversidadeService(db_session)
        universidade_data = UniversidadeCreate(nome="Universidade Para Ponto")
        universidade = await uni_service.create_universidade(universidade_data)
        
        unidade_service = UnidadeService(db_session)
        unidade_data = UnidadeCreate(
            nome="Unidade Para Ponto",
            universidade_id=universidade.id
        )
        unidade = await unidade_service.create_unidade(unidade_data)
        
        # Then create collection point
        ponto_service = PontoColetaService(db_session)
        ponto_data = PontoColetaCreate(
            nome="Ponto Teste",
            universidade_id=universidade.id,
            unidade_id=unidade.id
        )
        
        ponto = await ponto_service.create_ponto_coleta(ponto_data)
        
        assert ponto.id is not None
        assert ponto.nome == "Ponto Teste"
        assert ponto.universidade_id == universidade.id
        assert ponto.unidade_id == unidade.id
