from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, server_default=func.now())

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(String(500), nullable=True)
    local = Column(String(100), nullable=False)
    data_evento = Column(String(10), nullable=False)  # DD/MM/YYYY
    vagas = Column(Integer, nullable=False)
    cancelado = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now())
    organizador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)