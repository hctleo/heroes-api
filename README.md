# Hero's Missions Control API

API REST para cadastro de **heróis** e **missões**, construída com [FastAPI](https://fastapi.tiangolo.com/) e [SQLModel](https://sqlmodel.tiangolo.com/).

Este repositório foi criado para as aulas de **Introdução ao Desenvolvimento Backend** da disciplina de **Programação Avançada (turma 2026.2)** do curso de **Bacharelado em Engenharia Mecatrônica** do **IFCE – Campus Fortaleza**.

---

## Como executar

### Pré-requisitos

- [Python](https://www.python.org/downloads/) **3.14** ou superior
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recomendado) **ou** `pip`

### Opção 1: usando `uv` (recomendado)

```bash
# Instala as dependências (cria o ambiente virtual .venv automaticamente)
uv sync

# Inicia o servidor em modo de desenvolvimento (com recarregamento automático)
uv run fastapi dev main.py
```

### Opção 2: usando `pip` e `venv`

```bash
# Cria e ativa o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instala as dependências
pip install "fastapi[standard]" sqlmodel

# Inicia o servidor em modo de desenvolvimento
fastapi dev main.py
```

### Acessando a API

Com o servidor rodando, acesse:

| Recurso                          | URL                          |
| -------------------------------- | ---------------------------- |
| API                              | http://127.0.0.1:8000        |
| Documentação interativa (Swagger) | http://127.0.0.1:8000/docs   |
| Documentação alternativa (ReDoc)  | http://127.0.0.1:8000/redoc  |

> O banco de dados SQLite (`database.db`) e suas tabelas são criados automaticamente na inicialização da aplicação.

Para rodar em modo de produção, use `fastapi run main.py` (ou `uv run fastapi run main.py`).

---

## Estrutura do projeto

```
heroes-api/
├── main.py              # Ponto de entrada: cria a aplicação e registra as rotas
├── database.py          # Conexão com o SQLite e dependência de sessão
├── pyproject.toml       # Metadados e dependências do projeto
├── shared/
│   └── models.py        # Modelo base (id, created_at, updated_at, deleted_at)
└── modules/
    ├── hero/            # Módulo de heróis
    │   ├── models.py    # Tabela do banco de dados
    │   ├── schemas.py   # Esquemas de entrada e saída (validação)
    │   ├── service.py   # Regras de negócio
    │   └── routes.py    # Endpoints HTTP
    └── mission/         # Módulo de missões (mesma organização)
```

Cada módulo segue a separação em camadas **models → schemas → service → routes**, isolando o acesso ao banco, a validação dos dados, a lógica de negócio e a camada HTTP.

---

## Endpoints

### Heróis (`/hero`)

| Método   | Rota              | Descrição                         |
| -------- | ----------------- | --------------------------------- |
| `POST`   | `/hero/`          | Cadastra um herói                 |
| `GET`    | `/hero/`          | Lista heróis (`offset`, `limit`)  |
| `GET`    | `/hero/{hero_id}` | Busca um herói pelo Id            |
| `PATCH`  | `/hero/{hero_id}` | Atualiza parcialmente um herói    |
| `DELETE` | `/hero/{hero_id}` | Remove um herói (*soft delete*)   |

### Missões (`/mission`)

| Método   | Rota                    | Descrição                          |
| -------- | ----------------------- | ---------------------------------- |
| `POST`   | `/mission/`             | Cadastra uma missão                |
| `GET`    | `/mission/`             | Lista missões (`offset`, `limit`)  |
| `GET`    | `/mission/{mission_id}` | Busca uma missão pelo Id           |
| `PATCH`  | `/mission/{mission_id}` | Atualiza parcialmente uma missão   |
| `DELETE` | `/mission/{mission_id}` | Remove uma missão (*soft delete*)  |

Uma missão pode ser associada a um herói pelo campo `hero_id`.

### Exemplo de requisição

```bash
curl -X POST http://127.0.0.1:8000/hero/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Spider-Boy", "age": 18, "secret_name": "Pedro Parqueador"}'
```

---

## Conceitos abordados

- Criação de APIs REST com FastAPI
- Modelagem de dados e ORM com SQLModel
- Validação de dados com Pydantic
- Injeção de dependências (sessão do banco de dados)
- Relacionamentos entre tabelas (um herói possui várias missões)
- Paginação com `offset` e `limit`
- *Soft delete* (exclusão lógica)
- Tratamento de erros com `HTTPException`
