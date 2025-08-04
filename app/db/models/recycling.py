from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Numeric, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

# Tabela de associação para many-to-many entre PedidoDoacao e User (alunos)
pedido_doacao_alunos = Table(
    'pedido_doacao_alunos',
    Base.metadata,
    Column('pedido_doacao_id', Integer, ForeignKey('pedidos_doacao.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class TipoResiduo(Base):
    __tablename__ = "tipos_residuo"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    
    # Relacionamentos
    lancamentos = relationship("LancamentoResiduo", back_populates="tipo_residuo")


class PontoColeta(Base):
    __tablename__ = "pontos_coleta"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidades.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    responsavel_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    universidade = relationship("Universidade", back_populates="pontos_coleta")
    unidade = relationship("Unidade", back_populates="pontos_coleta")
    responsavel = relationship("User", back_populates="pontos_coleta_responsavel")
    lancamentos = relationship("LancamentoResiduo", back_populates="ponto_coleta")


class PedidoDoacao(Base):
    __tablename__ = "pedidos_doacao"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, nullable=False)
    criado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    criado_em = Column(DateTime, server_default=func.now())
    confirmado = Column(Boolean, default=False)
    
    # Relacionamentos
    criado_por = relationship("User", back_populates="pedidos_doacao_criados")
    turma = relationship("Turma", back_populates="pedidos_doacao")
    alunos = relationship(
        "User", 
        secondary=pedido_doacao_alunos,
        back_populates="doacoes_aluno"
    )
    lancamento = relationship("LancamentoResiduo", back_populates="pedido", uselist=False)


class LancamentoResiduo(Base):
    __tablename__ = "lancamentos_residuo"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos_doacao.id"), nullable=False, unique=True)
    ponto_coleta_id = Column(Integer, ForeignKey("pontos_coleta.id"), nullable=False)
    tipo_residuo_id = Column(Integer, ForeignKey("tipos_residuo.id"), nullable=False)
    peso_kg = Column(Numeric(6, 2), nullable=False)
    data = Column(DateTime, server_default=func.now())
    
    # Relacionamentos
    pedido = relationship("PedidoDoacao", back_populates="lancamento")
    ponto_coleta = relationship("PontoColeta", back_populates="lancamentos")
    tipo_residuo = relationship("TipoResiduo", back_populates="lancamentos")
