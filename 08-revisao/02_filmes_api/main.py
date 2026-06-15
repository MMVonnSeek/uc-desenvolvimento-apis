from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
import models
import schemas

# Criar as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Filmes")

@app.post("/filmes", response_model=schemas.FilmeResponse, status_code=status.HTTP_201_CREATED)
def criar_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    novo_filme = models.Filme(**filme.model_dump())
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

@app.get("/filmes", response_model=List[schemas.FilmeResponse])
def listar_filmes(db: Session = Depends(get_db)):
    return db.query(models.Filme).filter(models.Filme.ativo == True).all()

@app.get("/filmes/{filme_id}", response_model=schemas.FilmeResponse)
def buscar_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(models.Filme).filter(
        models.Filme.id == filme_id,
        models.Filme.ativo == True
    ).first()
    
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@app.patch("/filmes/{filme_id}", response_model=schemas.FilmeResponse)
def atualizar_filme(filme_id: int, filme_patch: schemas.FilmePatch, db: Session = Depends(get_db)):
    filme = db.query(models.Filme).filter(
        models.Filme.id == filme_id,
        models.Filme.ativo == True
    ).first()
    
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    update_data = filme_patch.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(filme, field, value)
    
    db.commit()
    db.refresh(filme)
    return filme

@app.delete("/filmes/{filme_id}")
def remover_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(models.Filme).filter(
        models.Filme.id == filme_id,
        models.Filme.ativo == True
    ).first()
    
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    filme.ativo = False
    db.commit()
    return {"mensagem": f"Filme {filme_id} removido com sucesso"}

# BÔNUS
@app.get("/filmes/melhores", response_model=List[schemas.FilmeResponse])
def melhores_filmes(db: Session = Depends(get_db)):
    return db.query(models.Filme).filter(
        models.Filme.nota >= 8.0,
        models.Filme.ativo == True
    ).order_by(models.Filme.nota.desc()).all()