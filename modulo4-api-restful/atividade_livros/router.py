from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Livro
from schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get(
    "/buscar",
    response_model=List[LivroResponse],
    tags=["Livros"],
    summary="Buscar livros por título",
    responses={
        status.HTTP_200_OK: {
            "description": "Lista de livros cujo título corresponde ao termo informado."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Parâmetro de consulta `titulo` ausente ou inválido."
        },
    },
)
def buscar_livros(titulo: str, db: Session = Depends(get_db)):
    livros = db.query(Livro).filter(Livro.titulo.ilike(f"%{titulo}%")).all()
    return livros


@router.get(
    "",
    response_model=List[LivroResponse],
    tags=["Livros"],
    summary="Listar livros disponíveis",
    responses={
        status.HTTP_200_OK: {
            "description": "Lista de livros ativos e disponíveis (`disponivel = True`)."
        }
    },
)
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(Livro).filter(Livro.disponivel == True).all()
    return livros


@router.get(
    "/{id}",
    response_model=LivroResponse,
    tags=["Livros"],
    summary="Obter livro por ID",
    responses={
        status.HTTP_200_OK: {"description": "Detalhes do livro encontrado."},
        status.HTTP_404_NOT_FOUND: {"description": "Livro não encontrado."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "ID inválido (deve ser inteiro)."},
    },
)
def obter_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )
    return livro


@router.post(
    "",
    response_model=LivroResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Livros"],
    summary="Cadastrar novo livro",
    responses={
        status.HTTP_201_CREATED: {"description": "Livro criado com sucesso."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Dados de entrada inválidos conforme `LivroCreate`."
        },
    },
)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = Livro(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.patch(
    "/{id}",
    response_model=LivroResponse,
    tags=["Livros"],
    summary="Atualizar livro parcialmente",
    responses={
        status.HTTP_200_OK: {"description": "Livro atualizado com sucesso."},
        status.HTTP_404_NOT_FOUND: {"description": "Livro não encontrado."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "ID ou payload de atualização inválido."
        },
    },
)
def atualizar_livro(id: int, livro_data: LivroUpdate, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    dados_atualizacao = livro_data.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizacao.items():
        setattr(livro, chave, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete(
    "/{id}",
    response_model=LivroResponse,
    tags=["Livros"],
    summary="Remover livro (soft delete)",
    responses={
        status.HTTP_200_OK: {
            "description": "Livro desativado (`disponivel = False`) e retornado."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Livro não encontrado."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "ID inválido (deve ser inteiro)."},
    },
)
def deletar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    livro.disponivel = False
    db.commit()
    db.refresh(livro)
    return livro

# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from database import get_db
# from models import Livro
# from schemas import LivroCreate, LivroResponse, LivroUpdate

# router = APIRouter(prefix="/livros", tags=["Livros"])


# # BÔNUS: Endpoint de busca por título (declarado antes de /{id} para evitar conflito de rotas)
# @router.get("/buscar", response_model=List[LivroResponse])
# def buscar_livros(titulo: str, db: Session = Depends(get_db)):
#     livros = db.query(Livro).filter(Livro.titulo.ilike(f"%{titulo}%")).all()
#     return livros


# @router.get("", response_model=List[LivroResponse])
# def listar_livros(db: Session = Depends(get_db)):
#     # Retorna todos os livros disponíveis (disponivel = True)
#     livros = db.query(Livro).filter(Livro.disponivel == True).all()
#     return livros


# @router.get("/{id}", response_model=LivroResponse)
# def obter_livro(id: int, db: Session = Depends(get_db)):
#     livro = db.query(Livro).filter(Livro.id == id).first()
#     if not livro:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Livro não encontrado",
#         )
#     return livro


# @router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
# def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
#     novo_livro = Livro(**livro.model_dump())
#     db.add(novo_livro)
#     db.commit()
#     db.refresh(novo_livro)
#     return novo_livro


# @router.patch("/{id}", response_model=LivroResponse)
# def atualizar_livro(id: int, livro_data: LivroUpdate, db: Session = Depends(get_db)):
#     livro = db.query(Livro).filter(Livro.id == id).first()
#     if not livro:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Livro não encontrado",
#         )

#     dados_atualizacao = livro_data.model_dump(exclude_unset=True)
#     for chave, valor in dados_atualizacao.items():
#         setattr(livro, chave, valor)

#     db.commit()
#     db.refresh(livro)
#     return livro


# @router.delete("/{id}", response_model=LivroResponse)
# def deletar_livro(id: int, db: Session = Depends(get_db)):
#     livro = db.query(Livro).filter(Livro.id == id).first()
#     if not livro:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Livro não encontrado",
#         )

#     # Soft delete: altera disponivel para False
#     livro.disponivel = False
#     db.commit()
#     db.refresh(livro)
#     return livro