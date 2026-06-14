from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import random

from database import engine, Base, get_db
from models import Usuario, Produto, Pedido, ItemPedido, Pagamento
from schemas import (
    UsuarioCreate, UsuarioResponse, LoginRequest, TokenResponse,
    ProdutoCreate, ProdutoPatch, ProdutoResponse,
    ItemCreate, PedidoResponse, PagamentoCreate, PagamentoResponse
)
from auth import criar_hash, verificar_senha, criar_token, usuario_logado
from tags import tags_metadata

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Projeto Final - API de Pagamentos - E-commerce",
    description="""
    ## API REST para E-commerce com Sistema de Pagamentos
    
    Esta API simula o back-end de uma loja virtual completa com:
    - Catálogo de produtos
    - Carrinho de compras (pedidos)
    - Sistema de pagamentos com múltiplos métodos
    - Autenticação JWT
    - Controle de estoque
    
    ### Como usar
    1. **Crie uma conta** em `POST /auth/registro`
    2. **Faça login** em `POST /auth/login` e copie o token
    3. **Clique em Authorize** (cadeado verde) e cole o token
    4. **Explore os endpoints** seguindo a ordem lógica de uma compra
    
    ### Tornar um usuário ADMIN
    Após criar um usuário, acesse o arquivo `data/ecommerce.db` e altere o campo `admin` para `1` na tabela `usuarios`.
    """,
    version="2.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Max Muller",
        "email": "max@senai.com",
    },
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints de saúde

@app.get("/", tags=["Saúde"], summary="Status da API")
def root():
    return {"status": "online", "versao": "2.0.0", "mensagem": "API de Pagamentos - E-commerce SENAI"}


@app.get("/health", tags=["Saúde"], summary="Health check")
def health_check():
    return {"status": "healthy"}


# Endpoints de autenticação

@app.post("/auth/registro", response_model=UsuarioResponse, status_code=201, tags=["Autenticação"])
def registrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se e-mail já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(409, "E-mail já cadastrado")
    
    # Criar novo usuário
    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        hash_senha=criar_hash(dados.senha),
        admin=False,
        ativo=True
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/auth/login", response_model=TokenResponse, tags=["Autenticação"])
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.hash_senha):
        raise HTTPException(401, "E-mail ou senha incorretos")
    
    token = criar_token({"sub": usuario.email, "admin": usuario.admin, "id": usuario.id})
    return {"access_token": token, "token_type": "bearer"}


# Dependência admin

def admin_required(usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)) -> Usuario:
    if not usuario.admin:
        raise HTTPException(403, "Acesso restrito a administradores")
    return usuario


# Endpoints de produtos

@app.get("/produtos", response_model=List[ProdutoResponse], tags=["Produtos"])
def listar_produtos(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    produtos = db.query(Produto).filter(Produto.ativo == True, Produto.estoque > 0).offset(skip).limit(limit).all()
    return produtos


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse, tags=["Produtos"])
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(404, "Produto não encontrado")
    return produto


@app.post("/produtos", response_model=ProdutoResponse, status_code=201, tags=["Produtos"])
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db), _: Usuario = Depends(admin_required)):
    novo_produto = Produto(**dados.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.patch("/produtos/{produto_id}", response_model=ProdutoResponse, tags=["Produtos"])
def atualizar_produto(produto_id: int, dados: ProdutoPatch, db: Session = Depends(get_db), _: Usuario = Depends(admin_required)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(404, "Produto não encontrado")
    
    update_data = dados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(produto, campo, valor)
    
    db.commit()
    db.refresh(produto)
    return produto


@app.delete("/produtos/{produto_id}", tags=["Produtos"])
def remover_produto(produto_id: int, db: Session = Depends(get_db), _: Usuario = Depends(admin_required)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(404, "Produto não encontrado")
    
    produto.ativo = False
    db.commit()
    return {"mensagem": f"Produto {produto_id} removido"}


# Endpoints de pedidos

@app.post("/pedidos", response_model=PedidoResponse, status_code=201, tags=["Pedidos"])
def criar_pedido(db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    novo_pedido = Pedido(usuario_id=usuario.id, status='aberto', total=0.0)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


@app.get("/pedidos", response_model=List[PedidoResponse], tags=["Pedidos"])
def listar_pedidos(db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    return db.query(Pedido).filter(Pedido.usuario_id == usuario.id).all()


@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse, tags=["Pedidos"])
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario.id).first()
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    return pedido


@app.post("/pedidos/{pedido_id}/itens", response_model=PedidoResponse, tags=["Pedidos"])
def adicionar_item(pedido_id: int, dados: ItemCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario.id).first()
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    if pedido.status != 'aberto':
        raise HTTPException(400, f"Pedido com status {pedido.status}")
    
    produto = db.query(Produto).filter(Produto.id == dados.produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(404, "Produto não encontrado")
    if produto.estoque < dados.quantidade:
        raise HTTPException(400, f"Estoque insuficiente: {produto.estoque}")
    
    subtotal = produto.preco * dados.quantidade
    item = ItemPedido(
        pedido_id=pedido_id,
        produto_id=dados.produto_id,
        quantidade=dados.quantidade,
        preco_unit=produto.preco,
        subtotal=subtotal
    )
    
    produto.estoque -= dados.quantidade
    pedido.total += subtotal
    
    db.add(item)
    db.commit()
    db.refresh(pedido)
    return pedido


@app.delete("/pedidos/{pedido_id}/itens/{item_id}", tags=["Pedidos"])
def remover_item(pedido_id: int, item_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario.id).first()
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    if pedido.status != 'aberto':
        raise HTTPException(400, f"Pedido com status {pedido.status}")
    
    item = db.query(ItemPedido).filter(ItemPedido.id == item_id, ItemPedido.pedido_id == pedido_id).first()
    if not item:
        raise HTTPException(404, "Item não encontrado")
    
    item.produto.estoque += item.quantidade
    pedido.total -= item.subtotal
    
    db.delete(item)
    db.commit()
    return {"mensagem": "Item removido"}


@app.patch("/pedidos/{pedido_id}/cancelar", tags=["Pedidos"])
def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario.id).first()
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    if pedido.status == 'pago':
        raise HTTPException(400, "Pedido já pago não pode ser cancelado")
    if pedido.status != 'aberto':
        raise HTTPException(400, f"Pedido com status {pedido.status}")
    
    for item in pedido.itens:
        item.produto.estoque += item.quantidade
    
    pedido.status = 'cancelado'
    db.commit()
    return {"mensagem": f"Pedido {pedido_id} cancelado"}


# ENDPOINTS DE PAGAMENTOS Endpoints de pagamentos

@app.post("/pedidos/{pedido_id}/pagar", response_model=PagamentoResponse, status_code=201, tags=["Pagamentos"])
def processar_pagamento(pedido_id: int, dados: PagamentoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_logado)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario.id).first()
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    if not pedido.itens:
        raise HTTPException(400, "Pedido vazio")
    if pedido.status != 'aberto':
        raise HTTPException(400, f"Pedido com status {pedido.status}")
    if pedido.pagamento:
        raise HTTPException(409, "Pagamento já existe")
    
    # Simular gateway
    metodo = dados.metodo
    status_pagamento = 'aprovado'
    if metodo == 'cartao_credito':
        status_pagamento = 'recusado' if random.random() < 0.1 else 'aprovado'
    
    codigo_transacao = str(uuid4())[:8].upper()
    
    pagamento = Pagamento(
        pedido_id=pedido_id,
        metodo=metodo,
        valor=pedido.total,
        status=status_pagamento,
        codigo_transacao=codigo_transacao
    )
    
    if status_pagamento == 'aprovado':
        pedido.status = 'pago'
    
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento