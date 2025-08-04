#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados iniciais
"""
import asyncio

from app.db.session import AsyncSessionLocal, engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models.institutional import Universidade, Unidade, Curso, Turma
from app.db.models.recycling import TipoResiduo
from app.core.security import get_password_hash


async def create_tables():
    """Criar todas as tabelas do banco"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_initial_data():
    """Criar dados iniciais no banco"""
    async with AsyncSessionLocal() as db:
        # Verificar se já existe um admin
        existing_admin = await db.get(User, 1)
        if existing_admin:
            print("Usuário administrador já existe")
            return
        
        # Criar universidade padrão
        universidade = Universidade(nome="Universidade Padrão")
        db.add(universidade)
        await db.flush()
        
        # Criar unidade padrão
        unidade = Unidade(
            nome="Campus Principal",
            universidade_id=universidade.id
        )
        db.add(unidade)
        await db.flush()
        
        # Criar curso padrão
        curso = Curso(
            nome="Administração",
            universidade_id=universidade.id,
            unidade_id=unidade.id
        )
        db.add(curso)
        await db.flush()
        
        # Criar turma padrão
        turma = Turma(
            nome="ADM2024",
            curso_id=curso.id,
            unidade_id=unidade.id,
            universidade_id=universidade.id
        )
        db.add(turma)
        await db.flush()
        
        # Criar usuário administrador
        admin_user = User(
            username="admin",
            email="admin@serrecicla.com",
            first_name="Administrador",
            last_name="Sistema",
            hashed_password=get_password_hash("admin123"),
            perfil="ADMIN_UNI",
            universidade_id=universidade.id,
            unidade_id=unidade.id,
            is_superuser=True,
            is_active=True
        )
        db.add(admin_user)
        
        # Criar tipos de resíduo padrão
        tipos_residuo = [
            TipoResiduo(nome="Papel"),
            TipoResiduo(nome="Plástico"), 
            TipoResiduo(nome="Metal"),
            TipoResiduo(nome="Vidro"),
            TipoResiduo(nome="Orgânico"),
            TipoResiduo(nome="Eletrônico")
        ]
        
        for tipo in tipos_residuo:
            db.add(tipo)
        
        await db.commit()
        print("Dados iniciais criados com sucesso!")
        print("Usuário administrador: admin / admin123")


async def main():
    """Função principal"""
    print("Criando tabelas...")
    await create_tables()
    
    print("Criando dados iniciais...")
    await create_initial_data()
    
    print("Inicialização concluída!")


if __name__ == "__main__":
    asyncio.run(main())
