from fastapi import FastAPI
import models
from database import engine
from router import router

# Cria as tabelas SQLite caso não existam
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livros",
    description="API RESTful de gerenciamento de acervo de livros com SQLite",
    version="1.0.0",
)

app.include_router(router)