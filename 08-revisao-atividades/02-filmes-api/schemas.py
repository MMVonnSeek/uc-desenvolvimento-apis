from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FilmeCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=200)
    diretor: str = Field(..., min_length=2, max_length=150)
    ano: Optional[int] = None
    nota: Optional[float] = Field(None, ge=0, le=10)

class FilmePatch(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=200)
    diretor: Optional[str] = Field(None, min_length=2, max_length=150)
    ano: Optional[int] = None
    nota: Optional[float] = Field(None, ge=0, le=10)

class FilmeResponse(BaseModel):
    id: int
    titulo: str
    diretor: str
    ano: Optional[int] = None
    nota: Optional[float] = None
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True