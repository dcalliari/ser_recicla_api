from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Universidade(Base):
    __tablename__ = "universidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    
    # Relacionamentos
    unidades = relationship("Unidade", back_populates="universidade", cascade="all, delete-orphan")
    cursos = relationship("Curso", back_populates="universidade")
    turmas = relationship("Turma", back_populates="universidade")
    users = relationship("User", back_populates="universidade")
    pontos_coleta = relationship("PontoColeta", back_populates="universidade")


class Unidade(Base):
    __tablename__ = "unidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidades.id"), nullable=False)
    
    # Relacionamentos
    universidade = relationship("Universidade", back_populates="unidades")
    cursos = relationship("Curso", back_populates="unidade")
    turmas = relationship("Turma", back_populates="unidade")
    users = relationship("User", back_populates="unidade")
    pontos_coleta = relationship("PontoColeta", back_populates="unidade")


class Curso(Base):
    __tablename__ = "cursos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidades.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    
    # Relacionamentos
    universidade = relationship("Universidade", back_populates="cursos")
    unidade = relationship("Unidade", back_populates="cursos")
    turmas = relationship("Turma", back_populates="curso")


class Turma(Base):
    __tablename__ = "turmas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidades.id"), nullable=False)
    
    # Relacionamentos
    curso = relationship("Curso", back_populates="turmas")
    unidade = relationship("Unidade", back_populates="turmas")
    universidade = relationship("Universidade", back_populates="turmas")
    users = relationship("User", back_populates="turma")
    pedidos_doacao = relationship("PedidoDoacao", back_populates="turma")
