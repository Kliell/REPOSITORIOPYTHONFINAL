from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Livro
from schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


# BÔNUS: Endpoint de busca por título (declarado antes de /{id} para evitar conflito de rotas)
@router.get("/buscar", response_model=List[LivroResponse])
def buscar_livros(titulo: str, db: Session = Depends(get_db)):
    livros = db.query(Livro).filter(Livro.titulo.ilike(f"%{titulo}%")).all()
    return livros


@router.get("", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    # Retorna todos os livros disponíveis (disponivel = True)
    livros = db.query(Livro).filter(Livro.disponivel == True).all()
    return livros


@router.get("/{id}", response_model=LivroResponse)
def obter_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )
    return livro


@router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = Livro(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.patch("/{id}", response_model=LivroResponse)
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


@router.delete("/{id}", response_model=LivroResponse)
def deletar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    # Soft delete: altera disponivel para False
    livro.disponivel = False
    db.commit()
    db.refresh(livro)
    return livro