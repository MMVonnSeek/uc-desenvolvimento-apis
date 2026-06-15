from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    diretor = Column(String(150), nullable=False)
    ano = Column(Integer, nullable=True)
    nota = Column(Float, nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())