# Import all models to ensure they are registered with SQLAlchemy
from app.db.models.institutional import Universidade, Unidade, Curso, Turma
from app.db.models.user import User
from app.db.models.recycling import TipoResiduo, PontoColeta, PedidoDoacao, LancamentoResiduo

__all__ = [
    "Universidade",
    "Unidade", 
    "Curso",
    "Turma",
    "User",
    "TipoResiduo",
    "PontoColeta", 
    "PedidoDoacao",
    "LancamentoResiduo"
]
