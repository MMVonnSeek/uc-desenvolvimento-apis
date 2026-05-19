from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Entrada: POST e PUT (campos obrigatorios)
class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    preco: float = Field(..., gt=0) # gt=0 - maior que zero
    estoque: int = Field(0, ge=0) # ge=0 - maior ou igual a zero

# Entrada: PATCH (todos os campos são opcionais)
class ProdutoPatch(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, ge=0)

# Saída: o que a API retorna
class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool
    criado_em: datetime

class Config:
    from_attributes = True # permite converter SQLAlchemy em Pydantic
    