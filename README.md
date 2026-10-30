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
pip install "fastapi[standard]" sqlmodel httpx

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

### Banco de dados (`database.db`)

A aplicação usa um banco SQLite no arquivo `database.db`, na raiz do projeto. Ele **não é versionado** (está no `.gitignore`), então é preciso criá-lo antes de usar a API. Basta iniciar o servidor uma vez: na inicialização, `create_db_and_tables()` cria o arquivo e todas as tabelas.

> **Atenção:** o `create_db_and_tables()` só cria tabelas que ainda não existem e **não altera** tabelas existentes. Se você já tinha um `database.db` de uma versão anterior do projeto (sem a coluna `photo_path` na tabela `hero`), apague o arquivo e reinicie o servidor para recriá-lo:
>
> ```bash
> rm database.db            # Linux/macOS
> # del database.db         # Windows
> uv run fastapi dev main.py
> ```
>
> Isso apaga todos os dados cadastrados.

As fotos enviadas pela API são salvas na pasta `uploads/`, criada automaticamente e também ignorada pelo Git.

Para rodar em modo de produção, use `fastapi run main.py` (ou `uv run fastapi run main.py`).

---

## Estrutura do projeto

```
heroes-api/
├── main.py              # Ponto de entrada: cria a aplicação e registra as rotas
├── database.py          # Conexão com o SQLite e dependência de sessão
├── http_client.py       # Cliente HTTP assíncrono (httpx) compartilhado e sua dependência
├── pyproject.toml       # Metadados e dependências do projeto
├── database.db          # Banco SQLite (gerado na inicialização, não versionado)
├── uploads/             # Fotos enviadas pela API (gerada automaticamente, não versionada)
├── shared/
│   └── models.py        # Modelo base (id, created_at, updated_at, deleted_at)
└── modules/
    ├── hero/            # Módulo de heróis
    │   ├── models.py    # Tabela do banco de dados
    │   ├── schemas.py   # Esquemas de entrada e saída (validação)
    │   ├── service.py   # Regras de negócio
    │   ├── routes.py    # Endpoints HTTP
    │   └── constants.py # Configuração do upload (pasta, formatos aceitos, tamanho máximo)
    ├── mission/         # Módulo de missões (mesma organização)
    └── villain/         # Módulo de vilões (consulta a uma API externa, sem banco)
        ├── constants.py # URL da SuperHero API
        ├── schemas.py   # Esquema de resposta
        ├── service.py   # Requisição à API externa e tratamento de erros
        └── routes.py    # Endpoints HTTP
```

Cada módulo segue a separação em camadas **models → schemas → service → routes**, isolando o acesso ao banco, a validação dos dados, a lógica de negócio e a camada HTTP.

O cliente `httpx.AsyncClient` é criado uma única vez no `lifespan` da aplicação (em `main.py`), guardado em `app.state` e injetado nas rotas pela dependência `HttpClientDep`. Assim, todas as requisições reaproveitam as mesmas conexões.

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
| `POST`   | `/hero/{hero_id}/photo` | Envia a foto de perfil (PNG/JPEG, até 2 MB) |
| `GET`    | `/hero/{hero_id}/photo` | Devolve a foto de perfil do herói |

### Missões (`/mission`)

| Método   | Rota                    | Descrição                          |
| -------- | ----------------------- | ---------------------------------- |
| `POST`   | `/mission/`             | Cadastra uma missão                |
| `GET`    | `/mission/`             | Lista missões (`offset`, `limit`)  |
| `GET`    | `/mission/{mission_id}` | Busca uma missão pelo Id           |
| `PATCH`  | `/mission/{mission_id}` | Atualiza parcialmente uma missão   |
| `DELETE` | `/mission/{mission_id}` | Remove uma missão (*soft delete*)  |

Uma missão pode ser associada a um herói pelo campo `hero_id`.

### Vilões (`/villain`)

| Método | Rota                    | Descrição                                                     |
| ------ | ----------------------- | ------------------------------------------------------------- |
| `GET`  | `/villain/{villain_id}` | Consulta um vilão na [SuperHero API](https://akabab.github.io/superhero-api/) (ex.: `655` = Thanos) |

Possíveis erros da consulta de vilões:

| Status | Quando acontece                                         |
| ------ | ------------------------------------------------------- |
| `404`  | Não existe vilão com o Id informado                     |
| `502`  | A API externa está inacessível ou respondeu com erro    |
| `504`  | A API externa demorou mais de 5 segundos para responder |

### Foto de perfil do herói

- Formatos aceitos: **PNG** e **JPEG** (caso contrário, `415 Unsupported Media Type`).
- Tamanho máximo: **2 MB** (caso contrário, `413 Content Too Large`).
- O arquivo é salvo em `uploads/` com um nome único (UUID), e o caminho fica no campo `photo_path` do herói.
- Enviar uma nova foto substitui a anterior, que é apagada do disco.
- `GET /hero/{hero_id}/photo` responde `404` se o herói não tiver foto.

### Exemplos de requisição

Cadastrar um herói:

```bash
curl -X POST http://127.0.0.1:8000/hero/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Spider-Boy", "age": 18, "secret_name": "Pedro Parqueador"}'
```

Enviar a foto de perfil (`multipart/form-data`, campo `file`):

```bash
curl -X POST http://127.0.0.1:8000/hero/<hero_id>/photo \
  -F "file=@foto.png"
```

Baixar a foto de perfil:

```bash
curl http://127.0.0.1:8000/hero/<hero_id>/photo --output foto.png
```

Consultar um vilão:

```bash
curl http://127.0.0.1:8000/villain/655
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
- Funções assíncronas com `async`/`await`
- Consumo de APIs externas com `httpx.AsyncClient`
- Envio de arquivos com `UploadFile` e `multipart/form-data`
- Devolução de arquivos com `FileResponse`
