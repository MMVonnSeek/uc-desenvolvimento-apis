from sqlalchemy import (
    Column, Integer, String, Float, Boolean, 
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    """Usuários do sistema (clientes e administradores)"""
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hash_senha = Column(String(200), nullable=False)
    admin = Column(Boolean, default=False)  # Administrador pode gerenciar produtos
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    pedidos = relationship('Pedido', back_populates='usuario', cascade='all, delete-orphan')


class Produto(Base):
    """Produtos disponíveis para compra"""
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    itens_pedido = relationship('ItemPedido', back_populates='produto')


class Pedido(Base):
    """Pedido de compra do usuário"""
    __tablename__ = 'pedidos'
    
    # Status: 'aberto' → 'pago' / 'cancelado'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(30), default='aberto')
    total = Column(Float, default=0.0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='pedidos')
    itens = relationship('ItemPedido', back_populates='pedido', cascade='all, delete-orphan')
    pagamento = relationship('Pagamento', back_populates='pedido', uselist=False, cascade='all, delete-orphan')


class ItemPedido(Base):
    """Item individual dentro de um pedido (tabela de junção)"""
    __tablename__ = 'itens_pedido'
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    preco_unit = Column(Float, nullable=False)  # Preço no momento da compra
    subtotal = Column(Float, nullable=False)    # quantidade * preco_unit
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    
    # Relacionamentos
    pedido = relationship('Pedido', back_populates='itens')
    produto = relationship('Produto', back_populates='itens_pedido')


class Pagamento(Base):
    """Pagamento vinculado a um pedido"""
    __tablename__ = 'pagamentos'
    
    # Métodos: 'pix' | 'cartao_credito' | 'boleto'
    # Status: 'aprovado' | 'recusado' | 'pendente'
    id = Column(Integer, primary_key=True, index=True)
    metodo = Column(String(20), nullable=False)
    status = Column(String(20), default='pendente')
    valor = Column(Float, nullable=False)
    codigo_transacao = Column(String(50), nullable=True)  # Gerado pelo gateway
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), unique=True)
    
    # Relacionamentos
    pedido = relationship('Pedido', back_populates='pagamento')