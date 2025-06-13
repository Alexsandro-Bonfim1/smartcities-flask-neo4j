# Smart Cities Network Analysis Backend

Este é um backend para análise de redes urbanas usando GraphQL, Flask e Neo4j.

## Requisitos

- Python 3.8+
- Neo4j (recomendado: versão 5.x)
- pip

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual (opcional mas recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sua_senha
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse o endpoint GraphQL em `http://localhost:5000/graphql`

## Funcionalidades

- CRUD de locais (nodes)
- CRUD de conexões entre locais (relationships)
- Consultas de rede
- Interface GraphiQL para testes

## Exemplos de Queries

### Listar todos os locais
```graphql
query {
  locations {
    id
    name
    type
    coordinates
    properties
  }
}
```

### Criar um novo local
```graphql
mutation {
  createLocation(
    name: "Praça Central"
    type: "Praça"
    coordinates: [40.7128, -74.0060]
    properties: { "population": 1000 }
  ) {
    location {
      id
      name
    }
  }
}
```

### Criar conexão entre locais
```graphql
mutation {
  createConnection(
    sourceId: "1"
    targetId: "2"
    type: "ROAD"
    properties: { "distance": 1000 }
  ) {
    connection {
      id
      type
    }
  }
}
```
