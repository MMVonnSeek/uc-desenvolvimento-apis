# Adicionar no main.py — importações necessárias
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title='API de Produtos SENAI', version='1.0.0')

# Banco de dados em memória (lista Python)
# Em produção: usaríamos SQLite, PostgreSQL, etc.
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3499.99, "estoque": 10},
    {"id": 2, "nome": "Mouse", "preco": 90.00, "estoque": 50},
    {"id": 3, "nome": "Teclado", "preco": 120.00, "estoque": 30}
]
proximo_id = 4  # controla o próximo ID

# ── Modelo Pydantic: define e valida os dados que entram ──────
# Quando o cliente fizer POST, o FastAPI vai verificar
# se o JSON tem 'nome' (str) e 'preco' (float) obrigatórios
class ProdutoCreate(BaseModel):
    nome:    str
    preco:   float
    estoque: int = 0  # opcional, padrão 0


# ════════════════════════════════════════════════════════
#  GET /produtos  →  lista todos os produtos
# ════════════════════════════════════════════════════════
@app.get('/produtos')
def listar_produtos():
    return produtos
# ════════════════════════════════════════════════════════
#  GET /produtos/{id}  →  busca um produto pelo ID
# ════════════════════════════════════════════════════════
@app.get('/produtos/{produto_id}')
def buscar_produto(produto_id: int):
    # Percorre a lista procurando o produto com aquele id
    produto = next(
        (p for p in produtos if p['id'] == produto_id),
        None  # valor padrão se não encontrar
    )
    if produto is None:
        return {'erro': f'Produto {produto_id} não encontrado'}
    return produto


# ════════════════════════════════════════════════════════
#  POST /produtos  →  cria um novo produto
# ════════════════════════════════════════════════════════
@app.post('/produtos', status_code=201)
def criar_produto(produto: ProdutoCreate):
    global proximo_id

    # Cria o novo produto com o próximo ID disponível
    novo_produto = {
        'id':      proximo_id,
        'nome':    produto.nome,
        'preco':   produto.preco,
        'estoque': produto.estoque,
    }
    produtos.append(novo_produto)
    proximo_id += 1

    # 201 Created — retornamos o produto criado com seu novo ID
    return novo_produto