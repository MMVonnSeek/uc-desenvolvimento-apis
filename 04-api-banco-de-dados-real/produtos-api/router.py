from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models   import Produto
from schemas  import ProdutoCreate, ProdutoPatch, ProdutoResponse

# APIRouter agrupa os endpoints - registramos no main.py
router = APIRouter(prefix='/produtos', tags=['Produtos'])

# GET/produtos - Lista todos os produtos
@router.get('/', response_model=List[ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 10,
                    db: Session = Depends(get_db)):
    return db.query(Produto).filter(Produto.ativo == True).offset(skip).limit(limit).all()

# GET/produtos/{id} - Busca produto pelo ID
@router.get('/{produto_id}', response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404,
                            detail=f'Produto {produto_id} não encontrado')
    return produto

# POST/produtos - Cria um produto
@router.post('/', response_model=ProdutoResponse, status_code=201)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(            
        nome    = dados.nome,
        preco   = dados.preco,
        estoque = dados.estoque,
    )
    db.add(produto)       # enfileira o INSERT
    db.commit()           # executa no banco
    db.refresh(produto)   # atualiza o objeto com id e criado_em do banco
    return produto

# PUT/produtos/{id} - Substitui o produto inteiro
@router.put('/{produto_id}', response_model=ProdutoResponse)
def substituir_produto(produto_id: int, dados: ProdutoCreate,
                        db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome    = dados.nome
    produto.preco   = dados.preco
    produto.estoque = dados.estoque
    db.commit()
    db.refresh(produto)
    return produto

# PATCH/produtos/{id} - Atualiza só os campos enviados
@router.patch('/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoPatch,
                       db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    if dados.nome    is not None: produto.nome    = dados.nome
    if dados.preco   is not None: produto.preco   = dados.preco
    if dados.estoque is not None: produto.estoque = dados.estoque
    db.commit()
    db.refresh(produto)
    return produto

# DELETE/produtos/{id} - marca ativo=False
@router.delete('/{produto_id}')
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.ativo = False   # soft delete: não apaga, apenas desativa
    db.commit()
    return {'mensagem': f'Produto {produto_id} removido com sucesso'}