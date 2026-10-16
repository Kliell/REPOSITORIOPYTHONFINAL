from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=200)
    autor: str = Field(..., min_length=2, max_length=150)
    ano_publicacao: Optional[int] = None
    disponivel: Optional[bool] = True


class LivroCreate(LivroBase):
    pass


class LivroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=200)
    autor: Optional[str] = Field(None, min_length=2, max_length=150)
    ano_publicacao: Optional[int] = None
    disponivel: Optional[bool] = None


class LivroResponse(LivroBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True