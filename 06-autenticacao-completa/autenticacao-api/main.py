from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models   import Usuario
from schemas  import UsuarioCreate, UsuarioPatch, UsuarioResponse, ErroResponse, LoginRequest, TokenResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import criar_hash, verificar_senha, criar_token, usuario_logado 
 
 
Base.metadata.create_all(bind=engine) 
 
app = FastAPI( 
    title='API de Usuários', 
    description='Demonstração de validação avançada com Pydantic', 
    version='1.0.0' 
) 
 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"],  # em produção: especifique os domínios 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 
 
# POST /usuarios - Cadastrar novo usuário 
# response_model=UsuarioResponse garante que a senha NUNCA vai 
# aparecer na resposta, mesmo que o objeto Usuario tenha hash_senha. 
@app.post("/auth/registro", response_model=UsuarioResponse, status_code=201) 
def registro(dados: UsuarioCreate, db: Session = Depends(get_db)): 
    if db.query(Usuario).filter(Usuario.email == dados.email).first(): 
        raise HTTPException(status_code=409, detail='E-mail já cadastrado') 
 
    # Em produção: hash_senha = bcrypt.hashpw(dados.senha...) 
    # Por enquanto guardamos a senha diretamente só para estudar o schema 
    # (no Capítulo 6 implementamos o bcrypt de verdade) 
    usuario = Usuario( 
        nome = dados.nome, 
        email = dados.email, 
        hash_senha = criar_hash(dados.senha),  # bcrypt d verdade 
    ) 
    db.add(usuario) 
    db.commit() 
    db.refresh(usuario) 
    return usuario   # FastAPI filtra pela UsuarioResponse — sem senha! 
 
@app.post("/auth/login", response_model=TokenResponse) 
def login(dados: LoginRequest, db: Session = Depends(get_db)): 
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first() 
 
    # Verifica email E senha juntos — nunca diga qual dos dois está errado 
    # (informar 'email não encontrado' ajuda atacantes a descobrir emails válidos) 
    if not usuario or not verificar_senha(dados.senha, usuario.hash_senha): 
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos") 
 
    # 'sub' é o campo padrão do JWT para identificar o dono do token 
    token = criar_token({"sub": usuario.email, "nome": usuario.nome}) 
    return {"access_token": token, "token_type": "bearer"} 
 
 
 
 
# GET /usuarios - Listar todos 
@app.get("/meu-perfil", response_model=UsuarioResponse) 
def meu_perfil(email: str = Depends(usuario_logado), db: Session = Depends(get_db)): 
    usuario = db.query(Usuario).filter(Usuario.email == email).first() 
    if not usuario: 
        raise HTTPException(status_code=404, detail="Usuário não encontrado") 
    return usuario 
 
 
 
# GET /usuarios/{id} - Buscar por ID 
@app.get("/usuarios", response_model=List[UsuarioResponse]) 
def listar_usuarios(db: Session = Depends(get_db)): 
    return db.query(Usuario).filter(Usuario.ativo == True).all() 
 
 
# PATCH /usuarios/{id} - Atualizar parcialmente 
@app.patch('/usuarios/{usuario_id}', response_model=UsuarioResponse) 
def atualizar(usuario_id: int, dados: UsuarioPatch, db: Session = Depends(get_db), email: str = 
Depends(usuario_logado),): 
 # Busca o usuário logado 
    atual = db.query(Usuario).filter(Usuario.email == email).first() 
    if not atual: 
        raise HTTPException( 
            status_code=401, detail="Usuário logado não encontrado no banco" 
        ) 
 
    if atual.id != usuario_id: 
        raise HTTPException(status_code=403, detail="Sem permissão") 
 
 
 
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first() 
    if not usuario: 
        raise HTTPException(status_code=404, detail='Usuário não encontrado') 
 
    if dados.nome  is not None: usuario.nome  = dados.nome 
    if dados.email is not None: usuario.email = dados.email 
    db.commit() 
    db.refresh(usuario) 
    return usuario 
 
 
# DELETE /usuarios/{id} - Soft delete 
@app.delete('/usuarios/{usuario_id}') 
def remover (usuario_id: int, db: Session = Depends(get_db)): 
    atual: Usuario = Depends(usuario_logado)
    if atual.id != usuario_id: 
                   raise HTTPException(status_code=403, detail='Sem permissão') 
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first() 
    if not usuario: 
        raise HTTPException(status_code=404, detail='Usuário não encontrado') 
    usuario.ativo = False 
    db.commit() 
    return {'mensagem': 'Conta desativada com sucesso'} 