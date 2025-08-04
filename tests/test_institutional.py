import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.institutional import UniversidadeService, UnidadeService
from app.schemas.institutional import UniversidadeCreate, UnidadeCreate


class TestInstitutional:
    
    @pytest.mark.asyncio
    async def test_create_universidade(self, db_session: AsyncSession):
        """Test creating a university"""
        service = UniversidadeService(db_session) 
        universidade_data = UniversidadeCreate(nome="Universidade Teste")
        
        universidade = await service.create_universidade(universidade_data)
        
        assert universidade.id is not None
        assert universidade.nome == "Universidade Teste"
    
    @pytest.mark.asyncio 
    async def test_get_all_universidades(self, db_session: AsyncSession):
        """Test getting all universities"""
        service = UniversidadeService(db_session)
        
        # Create test data
        universidade_data = UniversidadeCreate(nome="Universidade Teste 2")
        await service.create_universidade(universidade_data)
        
        universidades = await service.get_all_universidades()
        
        assert len(universidades) >= 1
        assert any(u.nome == "Universidade Teste 2" for u in universidades)
    
    @pytest.mark.asyncio
    async def test_create_unidade(self, db_session: AsyncSession):
        """Test creating a unit"""
        # First create a university
        uni_service = UniversidadeService(db_session)
        universidade_data = UniversidadeCreate(nome="Universidade Para Unidade")
        universidade = await uni_service.create_universidade(universidade_data)
        
        # Then create a unit
        unidade_service = UnidadeService(db_session)
        unidade_data = UnidadeCreate(
            nome="Unidade Teste",
            universidade_id=universidade.id
        )
        
        unidade = await unidade_service.create_unidade(unidade_data)
        
        assert unidade.id is not None
        assert unidade.nome == "Unidade Teste"
        assert unidade.universidade_id == universidade.id
