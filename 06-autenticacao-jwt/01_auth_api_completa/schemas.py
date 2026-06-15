from pydantic import BaseModel, Field, EmailStr, field_validator 
from typing import Optional 
from datetime import datetime 
 
class LoginRequest(BaseModel):  
    email: str  
    senha: str  
  
class TokenResponse(BaseModel):  
    access_token: str  
    token_type:   str = 'bearer' 
 
 
# Schema de CRIAÇÃO (POST) 
# Contém senha pois o usuário precisa enviar para se cadastrar. 
# NÃO contém id nem criado_em / o banco gera automaticamente. 
class UsuarioCreate(BaseModel): 
    nome: str = Field(..., min_length=2, max_length=100, description='Nome completo do usuário') 
    email: str = Field(..., description='E-mail válido - será usado no login') 
    senha: str = Field(..., min_length=8, description='Mínimo 8 caracteres') 
 
# @field_validator valida o campo 'nome' antes de salvar 
# Se a validação falhar: raise ValueError com a mensagem erro 
# Se passar: return v (o valor validado) 
    @field_validator('nome') 
    @classmethod 
    def nome_sem_numeros(cls, v: str) -> str: 
        if any(char.isdigit() for char in v): 
            raise ValueError('Nome não pode conter números') 
        if not v.strip(): 
            raise ValueError('Nome não pode ser só espaços') 
        return v.strip() # remove espaços extras das bordas 
 
    @field_validator('senha') 
    @classmethod 
    def senha_deve_ter_letra_e_numero(cls, v: str) -> str: 
        tem_letra = any(c.isalpha() for c in v) 
        tem_numero = any(c.isdigit() for c in v) 
        if not tem_letra or not tem_numero: 
            raise ValueError('Senha deve conter letras e números') 
        return v 
 
# Todos os campos são opcionais - o usuário envia só o que mudou 
# Não inclui senha - troca de senha seria um endpoint separado 
class UsuarioPatch(BaseModel): 
    nome: Optional[str] = Field(None, min_length=2, max_length=100) 
    email: Optional[EmailStr] = None 
 
    @field_validator('nome') 
    @classmethod 
    def nome_sem_numeros(cls, v): 
        if v and any(char.isdigit() for char in v): 
            raise ValueError('Nome não pode conter números') 
        return v.strip() if v else v 
 
# Schema de RESPOSTA (o que a API retorna) 
# NUNCA inclui hash_senha — mesmo com hash, nunca devolvemos. 
# Inclui id e criado_em — gerados pelo banco, úteis para o cliente. 
class UsuarioResponse(BaseModel): 
    id: int 
    nome: str 
    email: str 
    ativo: bool 
    criado_em: datetime 
 
    class Config: 
        from_attributes = True  # converte SQLAlchemy → Pydantic 
 
 
# Schema de ERRO PADRONIZADO 
# Usamos para retornar erros com formato consistente na API. 
class ErroResponse(BaseModel): 
    erro: str 
    detalhe: Optional[str] = None 