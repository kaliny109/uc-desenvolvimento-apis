from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# Schema de CRIAÇÃO (POST)
# Contém matricula pois o usuário precisa enviar para se cadastrar.
# NÃO contém id nem criado_em / o banco gera automaticamente.
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do aluno, 2-100 chars, sem números")
    email: EmailStr = Field(..., description="Email do aluno, deve ser um email válido")
    matricula: str = Field(..., min_length=8, max_length=8, description="obrigatório, exatamente 8 caracteres, apenas números")
    nota_final: Optional[float] = Field(0.0, ge=0.0, le=10.0, description="Nota final do aluno, entre 0.0 e 10.0")

    @field_validator('nome')
    @classmethod
    def nome_sem_numeros(cls, v: str) -> str:
       if any (char.isdigit() for char in v):
        raise ValueError("Nome não pode conter números")
       if not v.strip():
        raise ValueError("Nome não pode ser vazio")
       return v.strip()

    @field_validator('matricula')
    @classmethod
    def matricula_deve_ser_numerica(cls, v: str) -> str:
       tem_numero = any(c.isdigit() for c in v)
       if not (tem_numero):
        raise ValueError("Matrícula deve conter apenas números")
       return v 

class AlunoPatch(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


@field_validator('nome')
@classmethod
def nome_sem_numeros(cls, v):
    if v and any(char.isdigit() for char in v):
        raise ValueError("Nome não pode conter números")
    return v.strip() if v else v

# Schema de RESPOSTA (o que a API retorna)
# NUNCA inclui hash_senha — mesmo com hash, nunca devolvemos.
# Inclui id e criado_em — gerados pelo banco, úteis para o cliente..
class AlunoResponse(BaseModel):
    id: int
    nome: str
    email: str
    matricula: str
    nota_final: float
    criado_em: datetime

    class Config:
        from_attributes = True  # converte SQLAlchemy → Pydantic
        

# Schema de ERRO PADRONIZADO
# Usamos para retornar erros com formato consistente na API.
class ErroResponse(BaseModel):
    erro: str
    detalhe: Optional[str] = None