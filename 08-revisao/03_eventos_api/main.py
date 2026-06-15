from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from database import get_db, engine
import models
import schemas
from auth import (
    criar_token_acesso, verificar_senha, gerar_hash_senha,
    obter_usuario_logado, security
)

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Eventos")

# Endpoints de autenticação
@app.post("/auth/registro", response_model=schemas.UsuarioResponse, status_code=201)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    if usuario_existente:
        raise HTTPException(400, "Email já registrado")
    
    # Criar novo usuário
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/auth/login", response_model=schemas.Token)
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    # Buscar usuário pelo email
    usuario_db = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db.senha_hash):
        raise HTTPException(401, "Email ou senha incorretos")
    
    # Criar token JWT
    token = criar_token_acesso(
        data={"sub": str(usuario_db.id), "email": usuario_db.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}

# Dependência para obter o usuário completo do banco
def usuario_logado(
    db: Session = Depends(get_db),
    token_data: dict = Depends(obter_usuario_logado)
) -> models.Usuario:
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == token_data["id"]
    ).first()
    if not usuario:
        raise HTTPException(401, "Usuário não encontrado")
    return usuario

# Endpoints públicos de eventos 
@app.get("/eventos", response_model=List[schemas.EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    """Lista apenas eventos não cancelados"""
    return db.query(models.Evento).filter(
        models.Evento.cancelado == False
    ).all()

@app.get("/eventos/{evento_id}", response_model=schemas.EventoResponse)
def buscar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(
        models.Evento.id == evento_id,
        models.Evento.cancelado == False
    ).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    return evento

# Endpoints protegidos
@app.post("/eventos", response_model=schemas.EventoResponse, status_code=201)
def criar_evento(
    dados: schemas.EventoCreate,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(usuario_logado)
):
    """Cria evento associado ao usuário logado"""
    evento = models.Evento(
        **dados.model_dump(),
        organizador_id=atual.id
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

@app.patch("/eventos/{evento_id}", response_model=schemas.EventoResponse)
def editar_evento(
    evento_id: int,
    dados: schemas.EventoPatch,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(usuario_logado)
):
    """Apenas o organizador pode editar"""
    evento = db.query(models.Evento).filter(
        models.Evento.id == evento_id,
        models.Evento.cancelado == False
    ).first()
    
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    
    if evento.organizador_id != atual.id:
        raise HTTPException(403, "Sem permissão para editar este evento")
    
    update_data = dados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(evento, campo, valor)
    
    db.commit()
    db.refresh(evento)
    return evento

@app.delete("/eventos/{evento_id}")
def cancelar_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(usuario_logado)
):
    """Soft delete - apenas o organizador pode cancelar"""
    evento = db.query(models.Evento).filter(
        models.Evento.id == evento_id,
        models.Evento.cancelado == False
    ).first()
    
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    
    if evento.organizador_id != atual.id:
        raise HTTPException(403, "Sem permissão para cancelar este evento")
    
    evento.cancelado = True
    db.commit()
    return {"mensagem": f"Evento {evento_id} cancelado com sucesso"}

# ========== ENDPOINT BÔNUS ==========
@app.get("/meus-eventos", response_model=List[schemas.EventoResponse])
def meus_eventos(
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(usuario_logado)
):
    """Lista eventos criados pelo usuário logado"""
    return db.query(models.Evento).filter(
        models.Evento.organizador_id == atual.id,
        models.Evento.cancelado == False).all()