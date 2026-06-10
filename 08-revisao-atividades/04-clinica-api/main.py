from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
import models
import schemas
from auth import (
    criar_token_acesso, verificar_senha, gerar_hash_senha,
    obter_usuario_logado, security
)
from tags import tags_metadata

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Clínica Médica",
    description="API completa para gerenciamento de clínica médica com médicos, pacientes e consultas",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# Dependência de usúario logado
def usuario_logado(
    db: Session = Depends(get_db),
    token_data: dict = Depends(obter_usuario_logado)
) -> models.Usuario:
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == token_data["id"]
    ).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario

# Endpoints de autenticação
@app.post(
    "/auth/registro",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Autenticação"],
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário para acessar o sistema"
)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post(
    "/auth/login",
    response_model=schemas.Token,
    tags=["Autenticação"],
    summary="Login de usuário",
    description="Autentica um usuário e retorna um token JWT"
)
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    token = criar_token_acesso(
        data={"sub": str(usuario_db.id), "email": usuario_db.email}
    )
    return {"access_token": token, "token_type": "bearer"}

# Endpoints de médicos
@app.get(
    "/medicos",
    response_model=List[schemas.MedicoResponse],
    tags=["Médicos"],
    summary="Listar médicos",
    description="Retorna lista de todos os médicos ativos"
)
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).filter(models.Medico.ativo == True).all()

@app.get(
    "/medicos/{medico_id}",
    response_model=schemas.MedicoResponse,
    tags=["Médicos"],
    summary="Buscar médico por ID",
    description="Retorna os dados de um médico específico"
)
def buscar_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).filter(
        models.Medico.id == medico_id,
        models.Medico.ativo == True
    ).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico

@app.post(
    "/medicos",
    response_model=schemas.MedicoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Médicos"],
    summary="Criar médico",
    description="Cadastra um novo médico (requer autenticação)"
)
def criar_medico(
    dados: schemas.MedicoCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    # Verificar se CRM já existe
    crm_existente = db.query(models.Medico).filter(models.Medico.crm == dados.crm).first()
    if crm_existente:
        raise HTTPException(status_code=400, detail="CRM já cadastrado")
    
    medico = models.Medico(**dados.model_dump())
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico

@app.patch(
    "/medicos/{medico_id}",
    response_model=schemas.MedicoResponse,
    tags=["Médicos"],
    summary="Atualizar médico",
    description="Atualiza dados de um médico (requer autenticação)"
)
def atualizar_medico(
    medico_id: int,
    dados: schemas.MedicoPatch,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    update_data = dados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(medico, campo, valor)
    
    db.commit()
    db.refresh(medico)
    return medico

@app.delete(
    "/medicos/{medico_id}",
    tags=["Médicos"],
    summary="Desativar médico",
    description="Soft delete - desativa um médico (requer autenticação)"
)
def desativar_medico(
    medico_id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    medico.ativo = False
    db.commit()
    return {"mensagem": f"Médico {medico_id} desativado"}

# Endpoints de pacientes
@app.get(
    "/pacientes",
    response_model=List[schemas.PacienteResponse],
    tags=["Pacientes"],
    summary="Listar pacientes",
    description="Retorna lista de todos os pacientes ativos (requer autenticação)"
)
def listar_pacientes(db: Session = Depends(get_db), _: models.Usuario = Depends(usuario_logado)):
    return db.query(models.Paciente).filter(models.Paciente.ativo == True).all()

@app.get(
    "/pacientes/{paciente_id}",
    response_model=schemas.PacienteResponse,
    tags=["Pacientes"],
    summary="Buscar paciente por ID",
    description="Retorna os dados de um paciente específico (requer autenticação)"
)
def buscar_paciente(paciente_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(usuario_logado)):
    paciente = db.query(models.Paciente).filter(
        models.Paciente.id == paciente_id,
        models.Paciente.ativo == True
    ).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@app.post(
    "/pacientes",
    response_model=schemas.PacienteResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Pacientes"],
    summary="Criar paciente",
    description="Cadastra um novo paciente (requer autenticação)"
)
def criar_paciente(
    dados: schemas.PacienteCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    cpf_existente = db.query(models.Paciente).filter(models.Paciente.cpf == dados.cpf).first()
    if cpf_existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    paciente = models.Paciente(**dados.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

@app.patch(
    "/pacientes/{paciente_id}",
    response_model=schemas.PacienteResponse,
    tags=["Pacientes"],
    summary="Atualizar paciente",
    description="Atualiza dados de um paciente (requer autenticação)"
)
def atualizar_paciente(
    paciente_id: int,
    dados: schemas.PacientePatch,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    update_data = dados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(paciente, campo, valor)
    
    db.commit()
    db.refresh(paciente)
    return paciente

# Endpoints de consultas
@app.get(
    "/consultas",
    response_model=List[schemas.ConsultaResponse],
    tags=["Consultas"],
    summary="Listar consultas",
    description="Retorna lista de todas as consultas (requer autenticação)"
)
def listar_consultas(db: Session = Depends(get_db), _: models.Usuario = Depends(usuario_logado)):
    consultas = db.query(models.Consulta).all()
    # Enriquecer com nomes
    for consulta in consultas:
        if consulta.medico:
            consulta.medico_nome = consulta.medico.nome
        if consulta.paciente:
            consulta.paciente_nome = consulta.paciente.nome
    return consultas

@app.get(
    "/consultas/{consulta_id}",
    response_model=schemas.ConsultaResponse,
    tags=["Consultas"],
    summary="Buscar consulta por ID",
    description="Retorna os dados de uma consulta específica (requer autenticação)"
)
def buscar_consulta(consulta_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(usuario_logado)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    if consulta.medico:
        consulta.medico_nome = consulta.medico.nome
    if consulta.paciente:
        consulta.paciente_nome = consulta.paciente.nome
    return consulta

@app.post(
    "/consultas",
    response_model=schemas.ConsultaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Consultas"],
    summary="Criar consulta",
    description="Agenda uma nova consulta (requer autenticação)"
)
def criar_consulta(
    dados: schemas.ConsultaCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    # Verificar se médico existe
    medico = db.query(models.Medico).filter(
        models.Medico.id == dados.medico_id,
        models.Medico.ativo == True
    ).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Verificar se paciente existe
    paciente = db.query(models.Paciente).filter(
        models.Paciente.id == dados.paciente_id,
        models.Paciente.ativo == True
    ).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    consulta = models.Consulta(**dados.model_dump())
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    
    consulta.medico_nome = medico.nome
    consulta.paciente_nome = paciente.nome
    return consulta

@app.patch(
    "/consultas/{consulta_id}",
    response_model=schemas.ConsultaResponse,
    tags=["Consultas"],
    summary="Atualizar consulta",
    description="Atualiza dados de uma consulta (requer autenticação)"
)
def atualizar_consulta(
    consulta_id: int,
    dados: schemas.ConsultaPatch,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    update_data = dados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(consulta, campo, valor)
    
    db.commit()
    db.refresh(consulta)
    
    if consulta.medico:
        consulta.medico_nome = consulta.medico.nome
    if consulta.paciente:
        consulta.paciente_nome = consulta.paciente.nome
    return consulta

# Bônus
@app.get(
    "/medicos/{medico_id}/consultas",
    response_model=List[schemas.ConsultaResponse],
    tags=["Médicos", "Consultas"],
    summary="Consultas do médico",
    description="Retorna todas as consultas de um médico específico (requer autenticação)"
)
def consultas_do_medico(
    medico_id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    consultas = medico.consultas
    for consulta in consultas:
        consulta.medico_nome = medico.nome
        if consulta.paciente:
            consulta.paciente_nome = consulta.paciente.nome
    return consultas

@app.get(
    "/pacientes/{paciente_id}/consultas",
    response_model=List[schemas.ConsultaResponse],
    tags=["Pacientes", "Consultas"],
    summary="Histórico do paciente",
    description="Retorna todas as consultas de um paciente específico (requer autenticação)"
)
def consultas_do_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    consultas = paciente.consultas
    for consulta in consultas:
        if consulta.medico:
            consulta.medico_nome = consulta.medico.nome
        consulta.paciente_nome = paciente.nome
    return consultas

@app.patch(
    "/consultas/{consulta_id}/cancelar",
    response_model=schemas.ConsultaResponse,
    tags=["Consultas"],
    summary="Cancelar consulta",
    description="Cancela uma consulta sem necessidade de body (requer autenticação)"
)
def cancelar_consulta(
    consulta_id: int,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(usuario_logado)
):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    consulta.status = 'cancelada'
    db.commit()
    db.refresh(consulta)
    
    if consulta.medico:
        consulta.medico_nome = consulta.medico.nome
    if consulta.paciente:
        consulta.paciente_nome = consulta.paciente.nome
    return consulta