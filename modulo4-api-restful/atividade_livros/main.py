from fastapi import FastAPI
import models
from database import engine
from router import router
from tags import tags_metadata

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livros",
    description=(
        "API RESTful para gerenciamento de um acervo de livros utilizando **FastAPI**, "
        "**SQLAlchemy** e **SQLite**.\n\n"
        "### Principais recursos\n"
        "- Listagem de livros disponíveis (`disponivel = True`)\n"
        "- Busca por título com correspondência parcial (`ILIKE`)\n"
        "- Consulta detalhada por identificador (`id`)\n"
        "- Cadastro de novos livros (`201 Created`)\n"
        "- Atualização parcial de campos (`PATCH`)\n"
        "- Exclusão lógica (`soft delete`), marcando `disponivel = False`"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(router)

# from fastapi import FastAPI
# import models
# from database import engine
# from router import router

# # Cria as tabelas SQLite caso não existam
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="API de Livros",
#     description="API RESTful de gerenciamento de acervo de livros com SQLite",
#     version="1.0.0",
# )

# app.include_router(router)