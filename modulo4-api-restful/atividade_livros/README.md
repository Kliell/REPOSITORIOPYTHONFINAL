# 📚 API de Livros — FastAPI & SQLAlchemy

API RESTful desenvolvida em **Python** com **FastAPI**, **SQLAlchemy** e **SQLite** para gerenciamento de um acervo de livros. O projeto implementa operações completas de CRUD, busca parcial por título, exclusão lógica (*soft delete*) e documentação interativa via OpenAPI/Swagger UI.

---

## 📋 Sumário

1. [Visão Geral e Recursos](#-visão-geral-e-recursos)
2. [Estrutura do Projeto](#-estrutura-do-projeto)
3. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
4. [Configuração e Execução do Ambiente](#-configuração-e-execução-do-ambiente)
5. [Implementação da Documentação OpenAPI](#-implementação-da-documentação-openapi)
6. [Referência de Endpoints](#-referência-de-endpoints)
7. [Modelos de Dados (ORM e Schemas)](#-modelos-de-dados-orm-e-schemas)
8. [Validação no Swagger UI (`/docs`)](#-validação-no-swagger-ui-docs)
9. [Versionamento e Envio ao GitHub](#-versionamento-e-envio-ao-github)

---

## 🚀 Visão Geral e Recursos

A **API de Livros** permite administrar registros bibliográficos de forma simples e padronizada:

- **Listagem de Acervo Ativo:** Retorna apenas livros marcados como disponíveis (`disponivel = True`).
- **Busca por Título:** Pesquisa por correspondência parcial sem distinção de maiúsculas/minúsculas (`ILIKE`).
- **Consulta Individual:** Recupera os detalhes completos de um livro pelo seu identificador único (`id`).
- **Cadastro:** Insere novos livros validando tamanhos mínimos e máximos de campos via Pydantic.
- **Atualização Parcial (`PATCH`):** Altera apenas os campos informados na requisição (`exclude_unset=True`).
- **Exclusão Lógica (*Soft Delete*):** Desativa o livro (`disponivel = False`) preservando o histórico no banco de dados.

---

## 📁 Estrutura do Projeto

```text
atividade-livros-api/
├── .gitignore         # Arquivos e diretórios ignorados pelo Git (venv, __pycache__, *.db)
├── database.py        # Configuração da conexão SQLite, engine, SessionLocal e get_db()
├── main.py            # Ponto de entrada da aplicação FastAPI, criação das tabelas e metadados OpenAPI
├── models.py          # Modelo ORM SQLAlchemy da tabela `livros`
├── requirements.txt   # Dependências do projeto
├── router.py          # Definição das rotas /livros, regras de negócio e documentação de endpoints
├── schemas.py         # Schemas Pydantic para validação de entrada e serialização de saída
├── tags.py            # Definição das tags e descrições para agrupamento no Swagger UI
└── README.md          # Documentação do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** — Framework web moderno e de alta performance com geração automática de OpenAPI.
- **Uvicorn** — Servidor ASGI para execução da aplicação.
- **SQLAlchemy** — ORM para mapeamento objeto-relacional e comunicação com o SQLite.
- **Pydantic** — Validação de dados e serialização de schemas.
- **SQLite** — Banco de dados relacional leve baseado em arquivo (`livros.db`).

---

## ⚙️ Configuração e Execução do Ambiente

### 1. Clonar o repositório base (caso necessário)

```bash
git clone https://github.com/MMVonnSeek/dev-sistemas.git
```

Copie a pasta `modulo4-api-restful/atividade-livros-api` para o diretório do seu projeto e acesse-a pelo terminal.

### 2. Criar e ativar o ambiente virtual (`venv`)

```bash
python -m venv venv
```

* **Windows (Git Bash):**
  ```bash
  source venv/Scripts/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar as dependências e atualizar o `requirements.txt`

```bash
python -m pip install fastapi uvicorn sqlalchemy python-dotenv email-validator "python-jose[cryptography]" "passlib[bcrypt]" python-multipart "bcrypt==4.0.1"
python -m pip freeze > requirements.txt
```

### 4. Iniciar o servidor de desenvolvimento

```bash
python -m uvicorn main:app --reload
```

Com o servidor ativo, acesse:
- **Documentação Interativa (Swagger UI):** `http://127.0.0.1:8000/docs`
- **Documentação Alternativa (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## 🔌 Referência de Endpoints

Todas as rotas utilizam o prefixo `/livros`:

| Método | Rota | Resumo (`summary`) | Códigos HTTP | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/livros/buscar?titulo={texto}` | Buscar livros por título | `200`, `422` | Busca livros cujo título contenha o termo informado. |
| `GET` | `/livros` | Listar livros disponíveis | `200` | Lista todos os livros ativos (`disponivel = True`). |
| `GET` | `/livros/{id}` | Obter livro por ID | `200`, `404`, `422` | Retorna um livro específico pelo seu `id`. |
| `POST` | `/livros` | Cadastrar novo livro | `201`, `422` | Cria um novo registro de livro no banco de dados. |
| `PATCH` | `/livros/{id}` | Atualizar livro parcialmente | `200`, `404`, `422` | Atualiza parcialmente os campos enviados no JSON. |
| `DELETE` | `/livros/{id}` | Remover livro (soft delete) | `200`, `404`, `422` | Define `disponivel = False` sem remover o registro físico. |

### Exemplo de Payload (`POST /livros`)

```json
{
  "titulo": "Clean Code",
  "autor": "Robert C. Martin",
  "ano_publicacao": 2008,
  "disponivel": true
}
```

### Exemplo de Resposta (`201 Created`)

```json
{
  "titulo": "Clean Code",
  "autor": "Robert C. Martin",
  "ano_publicacao": 2008,
  "disponivel": true,
  "id": 1,
  "criado_em": "2026-11-23T14:00:00"
}
```

---

## 🗄️ Modelos de Dados (ORM e Schemas)

### Tabela `livros` (`models.py`)

| Campo | Tipo SQLAlchemy | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `primary_key=True`, `index=True` | Chave primária autoincremental |
| `titulo` | `String(200)` | `nullable=False` | Título da obra |
| `autor` | `String(150)` | `nullable=False` | Nome do autor |
| `ano_publicacao` | `Integer` | `nullable=True` | Ano de lançamento |
| `disponivel` | `Boolean` | `default=True` | Status de disponibilidade no acervo |
| `criado_em` | `DateTime(timezone=True)` | `server_default=func.now()` | Data e hora de cadastro |

### Regras de Validação (`schemas.py`)

- **`LivroCreate`**: `titulo` (2 a 200 caracteres), `autor` (2 a 150 caracteres), `ano_publicacao` (opcional), `disponivel` (opcional, padrão `True`).
- **`LivroUpdate`**: Todos os campos são opcionais, respeitando os mesmos limites de caracteres quando informados.
- **`LivroResponse`**: Inclui `id` e `criado_em`, com `from_attributes = True` habilitado para conversão direta do ORM.

---

## ✅ Validação no Swagger UI (`/docs`)

Após iniciar a aplicação e acessar `http://127.0.0.1:8000/docs`, verifique:

- [x] **Aba `Livros` separada:** Todos os endpoints estão agrupados sob a seção **Livros** com sua descrição exibida no cabeçalho da tag.
- [x] **`summary` visível na lista:** Cada rota apresenta seu título curto ao lado do método HTTP e do caminho.
- [x] **`responses` documentados:** Ao expandir qualquer rota, os códigos de status (`200`, `201`, `404`, `422`) aparecem na seção *Responses* com suas descrições.

---

## 🐙 Versionamento e Envio ao GitHub

Certifique-se de que o terminal esteja na pasta principal do projeto (`atividade-livros-api`) e que o `.gitignore` esteja presente para evitar o envio da pasta `venv/` e do arquivo `livros.db`:

```bash
git init
git add .
git commit -m "docs: documenta API de Livros com tags, summary, responses e README"
git push origin main
```