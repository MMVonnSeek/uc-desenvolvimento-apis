from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True),
                       server_default=func.now())
    
    def __repr__(self):
        return f'<Produto id={self.id} nome={self.nome}>'