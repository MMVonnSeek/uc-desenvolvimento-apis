from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime as dt
from typing import Optional

# Schemas de usúario
class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: dt

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schemas de evento
class EventoCreate(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=150)
    descricao: Optional[str] = Field(None, max_length=500)
    local: str = Field(..., min_length=3, max_length=100)
    data_evento: str
    vagas: int = Field(..., ge=1, le=1000)

    @field_validator('data_evento')
    @classmethod
    def validar_data(cls, v: str) -> str:
        try:
            dt.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Data deve estar no formato DD/MM/YYYY')
        return v

class EventoPatch(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=150)
    descricao: Optional[str] = Field(None, max_length=500)
    local: Optional[str] = Field(None, min_length=3, max_length=100)
    data_evento: Optional[str] = None
    vagas: Optional[int] = Field(None, ge=1, le=1000)

    @field_validator('data_evento')
    @classmethod
    def validar_data(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                dt.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError('Data deve estar no formato DD/MM/YYYY')
        return v

class EventoResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    local: str
    data_evento: str
    vagas: int
    cancelado: bool
    criado_em: dt
    organizador_id: int

    class Config:
        from_attributes = True