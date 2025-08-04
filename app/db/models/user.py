from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

from app.db.base import Base


class PerfilEnum(str, Enum):
    ADMIN_UNI = "ADMIN_UNI"
    COORD = "COORD"
    CHEFE = "CHEFE"
    ALUNO = "ALUNO"
    PONTO = "PONTO"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(254), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)
    
    # Campos específicos do sistema
    perfil = Column(String(10), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidades.id"), nullable=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
    
    # Relacionamentos
    universidade = relationship("Universidade", back_populates="users")
    unidade = relationship("Unidade", back_populates="users")
    turma = relationship("Turma", back_populates="users")
    
    # Relacionamentos de reciclagem
    pontos_coleta_responsavel = relationship("PontoColeta", back_populates="responsavel")
    pedidos_doacao_criados = relationship("PedidoDoacao", back_populates="criado_por")
    doacoes_aluno = relationship(
        "PedidoDoacao", 
        secondary="pedido_doacao_alunos",
        back_populates="alunos"
    )
