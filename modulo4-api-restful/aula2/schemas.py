from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=8)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("O nome não pode ser composto apenas por espaços.")
        if len(v) < 2 or len(v) > 100:
            raise ValueError("O nome deve ter entre 2 e 100 caracteres.")
        if any(char.isdigit() for char in v):
            raise ValueError("O nome não pode conter números.")
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres.")
        tem_letra = any(char.isalpha() for char in v)
        tem_numero = any(char.isdigit() for char in v)
        if not (tem_letra and tem_numero):
            raise ValueError("A senha deve conter pelo menos uma letra e um número.")
        return v


class UsuarioPatch(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("O nome não pode ser composto apenas por espaços.")
        if len(v) < 2 or len(v) > 100:
            raise ValueError("O nome deve ter entre 2 e 100 caracteres.")
        if any(char.isdigit() for char in v):
            raise ValueError("O nome não pode conter números.")
        return v


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class ErroResponse(BaseModel):
    erro: str
    detalhe: Optional[str] = None