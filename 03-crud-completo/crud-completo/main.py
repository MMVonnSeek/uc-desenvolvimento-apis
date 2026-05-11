from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API de Produtos",
    description="CRUD completo com FastAPI",
    version="1.0.0"    
)

produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "estoque": 10},
    {"id": 2, "nome": "Mouse", "preco": 89.90, "estoque": 50},
    {"id": 3, "nome": "Teclado", "preco": 120.00, "estoque": 30},
]
proximo_id = 4

class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    estoque: int = 0

class ProdutoPatch(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None

def encontrar_produto(produto_id: int):
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto is None:
        raise HTTPException(
            status_code=404,
            detail=f"Produto com id {produto_id} não encontrado"
        )
    return produto

@app.get('/produtos')
def listar_produtos():
    return produtos

@app.get('/produtos/{produto_id}')
def buscar_produto(produto_id: int):
    return encontrar_produto(produto_id)

@app.post('/produtos', status_code=201)
def criar_produto(produto: ProdutoCreate):
    global proximo_id
    novo = {
        'id': proximo_id,
        'nome': produto.nome,
        'preco': produto.preco,
        'estoque': produto.estoque,
    }
    produtos.append(novo)
    proximo_id += 1
    return novo

@app.put('/produtos/{produto_id}')
def substituir_produto(produto_id: int, dados: ProdutoCreate):
    produto = encontrar_produto(produto_id)
    produto['nome'] = dados.nome
    produto['preco'] = dados.preco
    produto['estoque'] = dados.estoque
    return produto

@app.patch('/produtos/{produto_id}')
def atualizar_produto(produto_id: int, dados: ProdutoPatch):
    produto = encontrar_produto(produto_id)
    if dados.nome is not None: produto['nome'] = dados.nome
    if dados.preco is not None: produto['preco'] = dados.preco
    if dados.estoque is not None: produto['estoque'] = dados.estoque
    return produto

@app.delete('/produtos/{produto_id}')
def remover_produto(produto_id: int):
    global produtos
    encontrar_produto(produto_id)
    produtos = [p for p in produtos if p['id'] != produto_id]
    return {'mensagem': f'Produto {produto_id} removido com sucesso'}