# Ser Recicla API - FastAPI Version

API para gerenciamento de reciclagem universitária reescrita com FastAPI.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados com tipagem
- **Alembic** - Migrações de banco de dados
- **JWT** - Autenticação via tokens
- **PostgreSQL/MySQL** - Banco de dados

## 📦 Instalação

### Método 1: Script Automático (Recomendado)

**Linux/macOS:**
```bash
chmod +x scripts/dev-setup.sh
./scripts/dev-setup.sh
```

**Windows:**
```cmd
scripts\dev-setup.bat
```

### Método 2: Manual

```bash
# Clone o repositório
git clone <repo-url>
cd ser_recicla_api

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -e ".[dev,test]"

# Configure o ambiente
cp .env.example .env
# Edite o arquivo .env conforme necessário

# Inicialize o banco de dados
python scripts/init_db.py
```

## ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

### Variáveis de Ambiente Principais

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development

# Banco de dados (escolha uma opção)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/ser_recicla_db
# DATABASE_URL=mysql+aiomysql://user:password@localhost/ser_recicla_db
# DATABASE_URL=sqlite+aiosqlite:///./test.db

JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=15

CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🗄️ Banco de Dados

### Inicialização
```bash
# Criar dados iniciais (usuário admin, tipos de resíduo, etc.)
python scripts/init_db.py
```

### Migrações com Alembic
```bash
# Gerar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### Usuário Administrador Padrão
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@serrecicla.com`
- **Perfil:** Administrador da Universidade

## 🏃‍♂️ Executando

### Desenvolvimento
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Iniciar servidor com hot reload
uvicorn app.main:app --reload

# Ou especificar host e porta
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
# Desenvolvimento com Docker Compose
docker-compose up --build

# Apenas a API
docker build -t ser-recicla-api .
docker run -p 8000:8000 ser-recicla-api
```

A API estará disponível em:
- **Documentação Swagger:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc
- **Health Check:** http://localhost:8000/api/v1/monitoring/healthcheck/

## 📋 API Endpoints

### Autenticação
- `POST /api/v1/auth/login/` - Login (retorna access_token e define refresh_token como cookie)
- `POST /api/v1/auth/refresh/` - Renovar access_token usando refresh_token do cookie
- `POST /api/v1/auth/logout/` - Logout (remove refresh_token cookie)
- `GET /api/v1/auth/me/` - Informações do usuário autenticado
- `POST /api/v1/auth/signup/coord/` - Cadastro de coordenador (requer ADMIN_UNI)
- `POST /api/v1/auth/signup/ponto/` - Cadastro de ponto de coleta (requer ADMIN_UNI)
- `POST /api/v1/auth/signup/chefe/` - Cadastro de chefe de turma (requer COORD)
- `POST /api/v1/auth/signup/aluno/` - Cadastro de aluno (requer CHEFE)

### Institucional
- `GET /api/v1/institutional/university/` - Listar universidades
- `POST /api/v1/institutional/university/` - Criar universidade (requer ADMIN_UNI)
- `GET /api/v1/institutional/unit/` - Listar unidades
- `POST /api/v1/institutional/unit/` - Criar unidade
- `GET /api/v1/institutional/course/` - Listar cursos
- `POST /api/v1/institutional/course/` - Criar curso
- `GET /api/v1/institutional/class/` - Listar turmas
- `POST /api/v1/institutional/class/` - Criar turma

### Reciclagem
- `GET /api/v1/recycling/tipo-residuo/` - Listar tipos de resíduo
- `POST /api/v1/recycling/tipo-residuo/` - Criar tipo de resíduo
- `GET /api/v1/recycling/pontos-coleta/` - Listar pontos de coleta (requer ADMIN_UNI)
- `POST /api/v1/recycling/pontos-coleta/` - Criar ponto de coleta (requer ADMIN_UNI)
- `GET /api/v1/recycling/ponto-coleta/{id}/` - Obter ponto específico (requer ADMIN_UNI)
- `PUT /api/v1/recycling/ponto-coleta/{id}/` - Atualizar ponto (requer ADMIN_UNI)
- `DELETE /api/v1/recycling/ponto-coleta/{id}/` - Deletar ponto (requer ADMIN_UNI)
- `GET /api/v1/recycling/pedido-doacao/` - Listar pedidos de doação (requer CHEFE)
- `POST /api/v1/recycling/pedido-doacao/` - Criar pedido de doação (requer CHEFE)
- `GET /api/v1/recycling/pedido-doacao/{id}/` - Obter pedido específico (requer CHEFE)
- `PUT /api/v1/recycling/pedido-doacao/{id}/` - Atualizar pedido (requer CHEFE)
- `DELETE /api/v1/recycling/pedido-doacao/{id}/` - Deletar pedido (requer CHEFE)
- `GET /api/v1/recycling/lancamento-residuo/` - Listar lançamentos (requer PONTO)
- `POST /api/v1/recycling/lancamento-residuo/` - Criar lançamento (requer PONTO)
- `GET /api/v1/recycling/lancamento-residuo/{id}/` - Obter lançamento (requer PONTO)
- `PUT /api/v1/recycling/lancamento-residuo/{id}/` - Atualizar lançamento (requer PONTO)
- `DELETE /api/v1/recycling/lancamento-residuo/{id}/` - Deletar lançamento (requer PONTO)

### Monitoramento
- `GET /api/v1/monitoring/healthcheck/` - Health check (público)

### Perfis de Usuário
- **ADMIN_UNI**: Administrador da Universidade
- **COORD**: Coordenador de Curso
- **CHEFE**: Chefe de Turma
- **ALUNO**: Aluno
- **PONTO**: Responsável pelo Ponto de Coleta

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura de código
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py
pytest tests/test_institutional.py
pytest tests/test_recycling.py

# Executar com verbose
pytest -v

# Executar testes em paralelo
pytest -n auto
```

## 🔧 Desenvolvimento

```bash
# Formatação de código
black app tests
isort app tests

# Linting
flake8 app tests

# Type checking
mypy app
```

## 📁 Estrutura do Projeto

```
.
├── app/                        # Código da aplicação
│   ├── api/                   # Rotas da API
│   │   └── v1/               # Versão 1 da API
│   │       ├── endpoints/    # Endpoints organizados por domínio
│   │       │   ├── auth.py          # Autenticação
│   │       │   ├── institutional.py # Gestão institucional
│   │       │   ├── recycling.py     # Gestão de reciclagem
│   │       │   └── monitoring.py    # Monitoramento
│   │       ├── api.py        # Router principal da API
│   │       └── dependencies.py      # Dependências da API v1
│   ├── core/                 # Configurações centrais
│   │   ├── config.py         # Configurações da aplicação
│   │   └── security.py       # Utilitários de segurança (JWT, hash)
│   ├── db/                   # Banco de dados
│   │   ├── base.py           # Classe base SQLAlchemy
│   │   ├── session.py        # Configuração de sessão
│   │   └── models/           # Modelos SQLAlchemy
│   │       ├── __init__.py
│   │       ├── user.py       # Modelo de usuário
│   │       ├── institutional.py    # Modelos institucionais
│   │       └── recycling.py  # Modelos de reciclagem
│   ├── schemas/              # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py          # Schemas de usuário
│   │   ├── institutional.py # Schemas institucionais
│   │   └── recycling.py     # Schemas de reciclagem
│   ├── services/             # Lógica de negócio
│   │   ├── auth.py          # Serviços de autenticação
│   │   ├── institutional.py # Serviços institucionais
│   │   └── recycling.py     # Serviços de reciclagem
│   ├── repositories/         # Acesso a dados
│   │   ├── user.py          # Repositório de usuários
│   │   ├── institutional.py # Repositórios institucionais
│   │   └── recycling.py     # Repositórios de reciclagem
│   ├── deps.py              # Dependências globais
│   └── main.py              # Aplicação FastAPI
├── tests/                   # Testes
│   ├── conftest.py         # Configurações de teste
│   ├── test_auth.py        # Testes de autenticação
│   ├── test_institutional.py # Testes institucionais
│   ├── test_recycling.py   # Testes de reciclagem
│   └── test_monitoring.py  # Testes de monitoramento
├── scripts/                 # Scripts utilitários
│   ├── init_db.py          # Inicialização do banco
│   ├── dev-setup.sh        # Setup de desenvolvimento (Linux/macOS)
│   └── dev-setup.bat       # Setup de desenvolvimento (Windows)
├── alembic/                 # Migrações do banco
│   ├── env.py              # Configuração do Alembic
│   └── versions/           # Arquivos de migração
├── alembic.ini             # Configuração do Alembic
├── pyproject.toml          # Configurações do projeto Python
├── docker-compose.yml      # Docker Compose para desenvolvimento
├── Dockerfile              # Imagem Docker da aplicação
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## 🏗️ Arquitetura

### Padrões Utilizados

- **Repository Pattern**: Camada de acesso a dados isolada
- **Service Layer**: Lógica de negócio centralizada
- **Dependency Injection**: Inversão de dependências via FastAPI
- **Schema Validation**: Validação robusta com Pydantic
- **Async/Await**: Operações assíncronas para melhor performance

### Fluxo de Dados

```
Request → Router → Service → Repository → Database
   ↓         ↓        ↓          ↓
Response ← Schema ← Model ← SQLAlchemy
```

1. **Router**: Recebe requisições HTTP e valida entrada
2. **Service**: Implementa regras de negócio
3. **Repository**: Abstrai acesso ao banco de dados
4. **Models**: Representam tabelas do banco (SQLAlchemy)
5. **Schemas**: Validam e serializam dados (Pydantic)
