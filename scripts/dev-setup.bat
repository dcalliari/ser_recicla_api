@echo off
REM Script de desenvolvimento para Windows - Ser Recicla API

echo 🚀 Configurando Ser Recicla API - FastAPI Version

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.11+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📥 Instalando dependências...
python -m pip install --upgrade pip
pip install -e ".[dev,test]"

REM Verificar se arquivo .env existe
if not exist ".env" (
    echo ⚙️ Criando arquivo .env...
    copy .env.example .env
    echo ✅ Arquivo .env criado. Configure as variáveis conforme necessário.
)

REM Inicializar banco de dados
echo 🗄️ Inicializando banco de dados...
python scripts/init_db.py

echo.
echo 🎉 Configuração concluída!
echo.
echo Para iniciar o servidor de desenvolvimento:
echo   venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload
echo.
echo Para executar os testes:
echo   pytest
echo.
echo Usuário administrador padrão:
echo   Username: admin
echo   Password: admin123
echo.
echo Documentação da API estará disponível em:
echo   http://localhost:8000/api/v1/docs

pause
