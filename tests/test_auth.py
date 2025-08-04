import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth import UserService
from app.schemas.user import UserCreate


class TestAuth:
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """Test creating a user"""
        service = UserService(db_session)
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            perfil="ALUNO"
        )
        
        user = await service.create_user(user_data, "ALUNO")
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.perfil == "ALUNO"
        assert user.is_active is True
    
    @pytest.mark.asyncio
    async def test_create_duplicate_user(self, db_session: AsyncSession):
        """Test creating a user with duplicate username raises error"""
        service = UserService(db_session)
        user_data = UserCreate(
            username="duplicate",
            email="duplicate1@example.com",
            password="testpass123",
            perfil="ALUNO"
        )
        
        # Create first user
        await service.create_user(user_data, "ALUNO")
        
        # Try to create duplicate
        user_data_duplicate = UserCreate(
            username="duplicate",  # Same username
            email="duplicate2@example.com",  # Different email
            password="testpass123",
            perfil="ALUNO"
        )
        
        with pytest.raises(Exception):  # Should raise HTTPException
            await service.create_user(user_data_duplicate, "ALUNO")
