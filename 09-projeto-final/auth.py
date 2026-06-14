from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-aqui-mude-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança Bearer
security = HTTPBearer(auto_error=False)


def criar_hash(senha: str) -> str:
    """Gera hash bcrypt da senha"""
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return pwd_context.verify(senha, hash_senha)


def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT com expiração"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def usuario_logado(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(lambda: None)  # Será substituído no main
):
    """
    Dependência para obter o usuário logado a partir do token JWT.
    Retorna o objeto Usuario ou lança 401.
    
    ATENÇÃO: Esta função precisa ser injetada com db no main.
    """
    from models import Usuario  # Importado aqui para evitar circular
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        admin: bool = payload.get("admin", False)
        
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    # Buscar usuário no banco
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    if not usuario.ativo:
        raise HTTPException(status_code=401, detail="Usuário desativado")
    
    return usuario