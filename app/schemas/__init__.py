from app.schemas.institutional import (
    Universidade, UniversidadeCreate, UniversidadeUpdate,
    Unidade, UnidadeCreate, UnidadeUpdate,
    Curso, CursoCreate, CursoUpdate,
    Turma, TurmaCreate, TurmaUpdate
)
from app.schemas.user import (
    User, UserCreate, UserUpdate, UserInfo,
    Token, TokenData
)
from app.schemas.recycling import (
    TipoResiduo, TipoResiduoCreate, TipoResiduoUpdate,
    PontoColeta, PontoColetaCreate, PontoColetaUpdate,
    PedidoDoacao, PedidoDoacaoCreate, PedidoDoacaoUpdate,
    LancamentoResiduo, LancamentoResiduoCreate, LancamentoResiduoUpdate
)

__all__ = [
    # Institutional
    "Universidade", "UniversidadeCreate", "UniversidadeUpdate",
    "Unidade", "UnidadeCreate", "UnidadeUpdate", 
    "Curso", "CursoCreate", "CursoUpdate",
    "Turma", "TurmaCreate", "TurmaUpdate",
    # User
    "User", "UserCreate", "UserUpdate", "UserInfo",
    "Token", "TokenData",
    # Recycling
    "TipoResiduo", "TipoResiduoCreate", "TipoResiduoUpdate",
    "PontoColeta", "PontoColetaCreate", "PontoColetaUpdate",
    "PedidoDoacao", "PedidoDoacaoCreate", "PedidoDoacaoUpdate", 
    "LancamentoResiduo", "LancamentoResiduoCreate", "LancamentoResiduoUpdate"
]
