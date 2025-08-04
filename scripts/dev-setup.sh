#!/bin/bash

# Script de desenvolvimento para configurar o projeto Ser Recicla API

set -e

echo "🚀 Configurando Ser Recicla API - FastAPI Version"

# Verificar se Python 3.11+ está instalado
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version encontrado"
else
    echo "❌ Python 3.11+ é necessário. Versão atual: $python_version"
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -e ".[dev,test]"

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Configure as variáveis conforme necessário."
fi

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
python scripts/init_db.py

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "Para iniciar o servidor de desenvolvimento:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Para executar os testes:"
echo "  pytest"
echo ""
echo "Usuário administrador padrão:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Documentação da API estará disponível em:"
echo "  http://localhost:8000/api/v1/docs"
