from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='API de Filmes', version='1.0.0')

filmes = [
    {"id": 1, "titulo": "Matrix", "diretor": "Wachowski", "ano": 1999, "nota": 9.0},
    {"id": 2, "titulo": "Interestelar", "diretor": "Nolan", "ano": 2014, "nota": 8.8},
    {"id": 3, "titulo": "De Volta para o Futuro", "diretor": "Zemeckis","ano": 1985, "nota": 9.2},
]
proximo_id = 4

class FilmeCreate(BaseModel):
    titulo:  str
    diretor: str
    ano:     int
    nota:    float

@app.get('/filmes')
def listar_filmes():
    return filmes

@app.get('/filmes/{filme_id}')
def buscar_filme(filme_id: int):
    filme = next((f for f in filmes if f['id'] == filme_id), None)
    if not filme:
        return {'erro': f'Filme {filme_id} não encontrado'}
    return filme

@app.post('/filmes', status_code=201)
def criar_filme(filme: FilmeCreate):
    global proximo_id
    novo = {
        'id':      proximo_id,
        'titulo':  filme.titulo,
        'diretor': filme.diretor,
        'ano':     filme.ano,
        'nota':    filme.nota,
    }
    filmes.append(novo)
    proximo_id += 1
    return novo