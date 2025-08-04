# Exemplos de uso da API Ser Recicla

## Configuração Base
```bash
export API_BASE_URL="http://localhost:8000/api/v1"
```

## 1. Health Check (Público)
```bash
curl -X GET "$API_BASE_URL/monitoring/healthcheck/"
```

## 2. Login
```bash
# Login com usuário padrão
curl -X POST "$API_BASE_URL/auth/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" \
  -c cookies.txt

# Resposta esperada:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "username": "admin"
# }
```

## 3. Obter informações do usuário
```bash
# Salvar o token de acesso
export ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "$API_BASE_URL/auth/me/" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## 4. Criar Universidade
```bash
curl -X POST "$API_BASE_URL/institutional/university/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Universidade Federal de Exemplo"
  }'
```

## 5. Listar Universidades
```bash
curl -X GET "$API_BASE_URL/institutional/university/" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## 6. Criar Unidade
```bash
curl -X POST "$API_BASE_URL/institutional/unit/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Campus Norte",
    "universidade_id": 1
  }'
```

## 7. Criar Tipo de Resíduo
```bash
curl -X POST "$API_BASE_URL/recycling/tipo-residuo/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Papel Reciclável"
  }'
```

## 8. Criar Ponto de Coleta (requer perfil ADMIN_UNI)
```bash
curl -X POST "$API_BASE_URL/recycling/pontos-coleta/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Ponto Central Campus Norte",
    "universidade_id": 1,
    "unidade_id": 1,
    "responsavel_id": null
  }'
```

## 9. Criar Usuário Coordenador
```bash
curl -X POST "$API_BASE_URL/auth/signup/coord/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "coord01",
    "email": "coordenador@exemplo.com",
    "password": "senha123",
    "first_name": "João",
    "last_name": "Coordenador",
    "perfil": "COORD",
    "universidade_id": 1,
    "unidade_id": 1
  }'
```

## 10. Refresh Token
```bash
curl -X POST "$API_BASE_URL/auth/refresh/" \
  -b cookies.txt \
  -c cookies.txt
```

## 11. Logout
```bash
curl -X POST "$API_BASE_URL/auth/logout/" \
  -b cookies.txt
```

## Exemplos com diferentes perfis

### Login como Coordenador
```bash
curl -X POST "$API_BASE_URL/auth/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=coord01&password=senha123" \
  -c cookies_coord.txt

export COORD_TOKEN="..." # Token retornado
```

### Criar Chefe de Turma (como coordenador)
```bash
curl -X POST "$API_BASE_URL/auth/signup/chefe/" \
  -H "Authorization: Bearer $COORD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "chefe01",
    "email": "chefe@exemplo.com", 
    "password": "senha123",
    "first_name": "Maria",
    "last_name": "Chefe",
    "perfil": "CHEFE",
    "universidade_id": 1,
    "unidade_id": 1,
    "turma_id": 1
  }'
```

### Criar Pedido de Doação (como chefe de turma)
```bash
# Primeiro, login como chefe
curl -X POST "$API_BASE_URL/auth/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=chefe01&password=senha123"

export CHEFE_TOKEN="..." # Token retornado

curl -X POST "$API_BASE_URL/recycling/pedido-doacao/" \
  -H "Authorization: Bearer $CHEFE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "DOA001",
    "turma_id": 1,
    "alunos": [2, 3, 4]
  }'
```

## Tratamento de Erros

### Token Expirado (401)
```bash
# Retorna:
# {
#   "detail": "Could not validate token"
# }
# Solução: Use o refresh token ou faça login novamente
```

### Permissão Insuficiente (403)
```bash
# Retorna:
# {
#   "detail": "Not enough permissions"
# }
# Solução: Use um usuário com o perfil adequado
```

### Recurso Não Encontrado (404)
```bash
# Retorna:
# {
#   "detail": "Resource not found"
# }
```

### Dados Inválidos (422)
```bash
# Retorna:
# {
#   "detail": [
#     {
#       "loc": ["body", "email"],
#       "msg": "field required",
#       "type": "value_error.missing"
#     }
#   ]
# }
```

## Scripts de Teste

### Teste Completo de Fluxo
```bash
#!/bin/bash
# Script para testar fluxo completo da API

API_BASE_URL="http://localhost:8000/api/v1"

echo "1. Testando health check..."
curl -s "$API_BASE_URL/monitoring/healthcheck/" | jq

echo "2. Fazendo login..."
RESPONSE=$(curl -s -X POST "$API_BASE_URL/auth/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123")

ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
echo "Token obtido: ${ACCESS_TOKEN:0:50}..."

echo "3. Obtendo informações do usuário..."
curl -s -X GET "$API_BASE_URL/auth/me/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq

echo "4. Listando universidades..."
curl -s -X GET "$API_BASE_URL/institutional/university/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq

echo "Teste concluído!"
```
