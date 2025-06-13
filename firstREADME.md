# Smart Cities Network Analysis Backend

Este é um backend para análise de redes urbanas usando GraphQL, Flask e Neo4j. O sistema permite modelar e analisar redes urbanas através de um banco de dados gráfico.

## Funcionalidades

- Gerenciamento de locais (nodes):
  - Criação, atualização e remoção de locais
  - Suporte a propriedades personalizadas
  - Tipos de localização (parques, edifícios, interseções, etc.)

- Gerenciamento de conexões (relationships):
  - Criação de conexões entre locais
  - Suporte a diferentes tipos de conexões (ruas, calçadas, etc.)
  - Propriedades personalizadas para conexões

- Análise de rede:
  - Cálculo de caminhos mais curtos
  - Métricas de rede
  - Filtragem por tipo de local
  - Busca por nome

## Requisitos

- Python 3.8+
- Neo4j (recomendado: versão 5.x)
- pip

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Alexsandro-Bonfim1/smartcities-flask-neo4j.git
cd smartcities-flask-neo4j
```

2. Crie um ambiente virtual (opcional mas recomendado):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
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

### Buscar local por nome
```graphql
query {
  locationByName(name: "Parque Central") {
    id
    name
    type
    coordinates
  }
}
```

### Listar locais por tipo
```graphql
query {
  locationsByType(type: "Parque") {
    id
    name
    type
    coordinates
  }
}
```

### Encontrar caminho mais curto
```graphql
query {
  shortestPath(sourceId: "1", targetId: "3") {
    id
    name
    type
  }
}
```

### Métricas da rede
```graphql
query {
  networkMetrics
}
```

### Criar novo local
```graphql
mutation {
  createLocation(
    name: "Parque Central"
    type: "Parque"
    coordinates: [-46.633309, -23.550520]
    properties: { area: 10000, facilities: ["playground", "fountains"] }
  ) {
    location {
      id
      name
      type
      coordinates
      properties
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
    properties: { distance: 1000, lanes: 4 }
  ) {
    connection {
      id
      type
      properties
    }
  }
}
```

### Atualizar local existente
```graphql
mutation {
  updateLocation(
    id: "1"
    name: "Parque Municipal"
    properties: { area: 15000, facilities: ["playground", "fountains", "gym"] }
  ) {
    id
    name
    type
    properties
  }
}
```

## Estrutura do Projeto

```
smartcities-flask-neo4j/
├── app.py           # Ponto de entrada da aplicação Flask
├── schema.py        # Definições do schema GraphQL
├── requirements.txt # Dependências do projeto
├── .env            # Variáveis de ambiente
└── .gitignore      # Arquivos ignorados pelo Git
```

## Tecnologias Utilizadas

- Flask: Framework web para Python
- GraphQL: Sistema de query para APIs
- Neo4j: Banco de dados gráfico
- Python: Linguagem de programação

## Contribuição

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
