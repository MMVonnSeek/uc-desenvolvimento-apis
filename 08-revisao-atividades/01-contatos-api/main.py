from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title='API de Contatos SENAI')

contatos = [
    {"id":1,"nome":"Alice Oliveira","telefone":"61999990001","email":"alice@email.com","favorito":True},
    {"id":2,"nome":"Breno Costa","telefone":"61999990002","email":"breno@email.com","favorito":False},
    {"id":3,"nome":"Camila Souza","telefone":"61999990003","email":"camila@email.com","favorito":True},
]
proximo_id = 4

class ContatoCreate(BaseModel):
    nome:     str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=7, max_length=20)
    email:    str
    favorito: bool = False

class ContatoPatch(BaseModel):
    nome:     Optional[str]  = Field(None, min_length=2, max_length=100)
    telefone: Optional[str]  = Field(None, min_length=7, max_length=20)
    email:    Optional[str]  = None
    favorito: Optional[bool] = None

def achar(cid):
    c = next((x for x in contatos if x['id']==cid), None)
    if not c: raise HTTPException(404, f'Contato {cid} não encontrado')
    return c

@app.get('/contatos')           # lista todos
def listar(): return contatos

@app.get('/contatos/favoritos') # bônus — antes do /{id}!
def favoritos(): return [c for c in contatos if c['favorito']]

@app.get('/contatos/{cid}')     # busca por id
def buscar(cid: int): return achar(cid)

@app.post('/contatos', status_code=201)
def criar(dados: ContatoCreate):
    global proximo_id
    novo = {'id':proximo_id,'nome':dados.nome,'telefone':dados.telefone,
            'email':dados.email,'favorito':dados.favorito}
    contatos.append(novo); proximo_id+=1
    return novo

@app.put('/contatos/{cid}')
def substituir(cid:int, dados:ContatoCreate):
    c = achar(cid)
    c['nome']=dados.nome; c['telefone']=dados.telefone
    c['email']=dados.email; c['favorito']=dados.favorito
    return c

@app.patch('/contatos/{cid}')
def atualizar(cid:int, dados:ContatoPatch):
    c = achar(cid)
    if dados.nome     is not None: c['nome']     = dados.nome
    if dados.telefone is not None: c['telefone'] = dados.telefone
    if dados.email    is not None: c['email']    = dados.email
    if dados.favorito is not None: c['favorito'] = dados.favorito
    return c

@app.patch('/contatos/{cid}/favoritar')  # bônus
def favoritar(cid:int):
    c = achar(cid)
    c['favorito'] = True
    return {'mensagem': f'{c["nome"]} marcado como favorito'}

@app.delete('/contatos/{cid}')
def remover(cid:int):
    global contatos
    achar(cid)
    contatos = [c for c in contatos if c['id']!=cid]
    return {'mensagem': f'Contato {cid} removido'}