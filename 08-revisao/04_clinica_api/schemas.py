from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime as dt
from typing import Optional, List

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

# Schemas de médico
class MedicoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    crm: str = Field(..., min_length=5, max_length=10)
    especialidade: str = Field(..., min_length=3, max_length=100)
    usuario_id: Optional[int] = None

    @field_validator('crm')
    @classmethod
    def crm_valido(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('CRM deve conter apenas dígitos')
        return v

class MedicoPatch(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=150)
    crm: Optional[str] = Field(None, min_length=5, max_length=10)
    especialidade: Optional[str] = Field(None, min_length=3, max_length=100)
    ativo: Optional[bool] = None

    @field_validator('crm')
    @classmethod
    def crm_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.isdigit():
            raise ValueError('CRM deve conter apenas dígitos')
        return v

class MedicoResponse(BaseModel):
    id: int
    nome: str
    crm: str
    especialidade: str
    ativo: bool
    criado_em: dt
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

# Schemas de pacientes
class PacienteCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: str
    telefone: Optional[str] = Field(None, max_length=20)

    @field_validator('cpf')
    @classmethod
    def cpf_valido(cls, v: str) -> str:
        if len(v) != 11 or not v.isdigit():
            raise ValueError('CPF deve ter exatamente 11 dígitos numéricos')
        return v

    @field_validator('data_nascimento')
    @classmethod
    def data_valida(cls, v: str) -> str:
        try:
            dt.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Data deve estar no formato DD/MM/YYYY')
        return v

class PacientePatch(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=150)
    telefone: Optional[str] = Field(None, max_length=20)
    ativo: Optional[bool] = None

class PacienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: str
    telefone: Optional[str] = None
    ativo: bool
    criado_em: dt

    class Config:
        from_attributes = True

# Schemas de consulta
class ConsultaCreate(BaseModel):
    data_consulta: str
    motivo: str = Field(..., min_length=5, max_length=300)
    status: str = 'agendada'
    medico_id: int
    paciente_id: int

    @field_validator('data_consulta')
    @classmethod
    def data_valida(cls, v: str) -> str:
        try:
            dt.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Data deve estar no formato DD/MM/YYYY')
        return v

    @field_validator('status')
    @classmethod
    def status_valido(cls, v: str) -> str:
        opcoes = ['agendada', 'realizada', 'cancelada']
        if v not in opcoes:
            raise ValueError(f'Status deve ser: {", ".join(opcoes)}')
        return v

class ConsultaPatch(BaseModel):
    data_consulta: Optional[str] = None
    motivo: Optional[str] = Field(None, min_length=5, max_length=300)
    status: Optional[str] = None

    @field_validator('data_consulta')
    @classmethod
    def data_valida(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                dt.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError('Data deve estar no formato DD/MM/YYYY')
        return v

    @field_validator('status')
    @classmethod
    def status_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            opcoes = ['agendada', 'realizada', 'cancelada']
            if v not in opcoes:
                raise ValueError(f'Status deve ser: {", ".join(opcoes)}')
        return v

class ConsultaResponse(BaseModel):
    id: int
    data_consulta: str
    motivo: str
    status: str
    criado_em: dt
    medico_id: int
    paciente_id: int
    medico_nome: Optional[str] = None
    paciente_nome: Optional[str] = None

    class Config:
        from_attributes = True