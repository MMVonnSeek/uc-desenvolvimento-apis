from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class AlunoCreate(BaseModel):
    nome:str = Field(..., min_length=2, max_length=100)
    email:EmailStr
    matricula:str = Field(..., min_length=8, max_length=8, description='Exatamente 8 digitos')
    nota_final:float = Field(0.0, ge=0, le=10)
    
    @field_validator('nome')
    @classmethod
    def nome_sem_numeros(cls, v):
        if any(c.isdigit() for c in v):
            raise ValueError('Nome não pode conter números')
        return v.strip()
    
    @field_validator('matricula')
    @classmethod
    def matricula_so_digitos(cls, v):
        if not v.isdigit():
            raise ValueError('Matricula deve conter apenas números')
        return v
    
class AlunoPatch(BaseModel):
    nota_final: Optional[float] = Field(None, ge=0, le=10)
    email: Optional[EmailStr] = None

class ErroResponse(BaseModel):
    detail: str

class AlunoResponse(BaseModel):
    id:int
    nome:str
    email:str
    matricula:str
    nota_final:float
    ativo:bool
    criado_em:datetime

    class Config:
        from_attributes = True
        