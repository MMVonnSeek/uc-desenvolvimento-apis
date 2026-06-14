from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
import re


# Schemas de usuário
class UsuarioCreate(BaseModel):
    """Schema para criação de usuário"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    email: EmailStr = Field(..., description="E-mail válido")
    senha: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    
    @field_validator('senha')
    @classmethod
    def senha_forte(cls, v: str) -> str:
        """Valida força da senha"""
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra')
        return v


class UsuarioResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    nome: str
    email: str
    admin: bool
    ativo: bool
    criado_em: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema para login"""
    email: str = Field(..., description="E-mail do usuário")
    senha: str = Field(..., description="Senha do usuário")


class TokenResponse(BaseModel):
    """Schema para resposta de token JWT"""
    access_token: str
    token_type: str = 'bearer'


# Schemas de produto
class ProdutoCreate(BaseModel):
    """Schema para criação de produto"""
    nome: str = Field(..., min_length=2, max_length=200, description="Nome do produto")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição detalhada")
    preco: float = Field(..., gt=0, description="Preço em reais (maior que 0)")
    estoque: int = Field(0, ge=0, description="Quantidade em estoque")
    
    @field_validator('preco')
    @classmethod
    def preco_valido(cls, v: float) -> float:
        """Arredonda preço para 2 casas decimais"""
        return round(v, 2)


class ProdutoPatch(BaseModel):
    """Schema para atualização parcial de produto"""
    nome: Optional[str] = Field(None, min_length=2, max_length=200)
    descricao: Optional[str] = Field(None, max_length=1000)
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, ge=0)
    ativo: Optional[bool] = None


class ProdutoResponse(BaseModel):
    """Schema para resposta de produto"""
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    estoque: int
    ativo: bool
    criado_em: datetime
    
    class Config:
        from_attributes = True


# Schemas de item do pedido
class ItemCreate(BaseModel):
    """Schema para adicionar item ao pedido"""
    produto_id: int = Field(..., gt=0, description="ID do produto")
    quantidade: int = Field(..., ge=1, description="Quantidade (mínimo 1)")


class ItemResponse(BaseModel):
    """Schema para resposta de item do pedido"""
    id: int
    quantidade: int
    preco_unit: float
    subtotal: float
    produto: ProdutoResponse
    
    class Config:
        from_attributes = True


# Schemas de pagamento
METODOS_VALIDOS = ['pix', 'cartao_credito', 'boleto']

class PagamentoCreate(BaseModel):
    """Schema para processar pagamento"""
    metodo: str = Field(..., description=f"Método de pagamento: {', '.join(METODOS_VALIDOS)}")
    
    @field_validator('metodo')
    @classmethod
    def metodo_valido(cls, v: str) -> str:
        v = v.lower()
        if v not in METODOS_VALIDOS:
            raise ValueError(f'Método inválido. Use: {", ".join(METODOS_VALIDOS)}')
        return v


class PagamentoResponse(BaseModel):
    """Schema para resposta de pagamento"""
    id: int
    metodo: str
    status: str
    valor: float
    codigo_transacao: Optional[str]
    criado_em: datetime
    
    class Config:
        from_attributes = True


# Schemas de pedido
class PedidoResponse(BaseModel):
    """Schema para resposta de pedido (completo)"""
    id: int
    status: str
    total: float
    criado_em: datetime
    itens: List[ItemResponse] = []
    pagamento: Optional[PagamentoResponse] = None
    
    class Config:
        from_attributes = True