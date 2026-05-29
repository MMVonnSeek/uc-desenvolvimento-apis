from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models   import Usuario
from schemas  import UsuarioCreate, UsuarioPatch, UsuarioResponse, ErroResponse, LoginRequest, TokenResponse
from auth import criar_hash, verificar_senha, criar_token, usuario_logado
from fastapi.middleware.cors import CORSMiddleware
from tags import tags_metadata

Base.metadata.create_all(bind=engine)

# Configuração do FastAPI - agora com metadados do Swagger
app = FastAPI(
    title='API de Usuários',
    description="""
## API REST de gerenciamento de usuários

Desenvolvida com **FastAPI** e **SQLAlchemy**.

### Como usar
1. Crie uma conta em `POST /auth/registro`
2. Faça login em `POST /auth/login` e copie o token
3. Clique em **Authorize** e cole o token
""",
    version='1.0.0',
    contact={"name": "Max Muller", "email": "max@emailsenai.com" },
    openapi_tags=tags_metadata
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# POST /usuarios - Cadastrar novo usuário
# response_model=UsuarioResponse garante que a senha NUNCA vai
# aparecer na resposta, mesmo que o objeto Usuario tenha hash_senha.
@app.post('/auth/registro',
          response_model=UsuarioResponse,
          status_code=201,
          tags=['Autenticação'],
          summary='Criar nova conta',
          description='Cria uma conta com nome, e-mail e senha. A senha é armazenada como hash bcrypt',
          responses={
               201: {'description': 'Conta criada com sucesso'},
               409: {'description': 'E-mail ja cadastrado'},
               422: {'description': 'Dados inválidos'}})
def registro(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica email duplicado antes de tentar inserir
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(
            status_code=409,
            detail='E-mail já cadastrado'
        )
    # Em produção: hash_senha = bcrypt.hashpw(dados.senha...)
    # Por enquanto guardamos a senha diretamente só para estudar o schema
    # (no Capítulo 6 implementamos o bcrypt de verdade)
    usuario = Usuario(
        nome = dados.nome,
        email = dados.email,
        hash_senha = criar_hash(dados.senha), # substituir por hash na aula 6
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario   # FastAPI filtra pela UsuarioResponse — sem senha!

@app.post('/auth/login', response_model=TokenResponse,
          tags=['Autenticação'],
          summary='Fazer login e Obter token JWT',
          description='Autentica o usuário e retorna um token JWT. Use o token no botão **Authorize**',
          responses={
               200: {'description': 'Login realizado - token retornado'},
               401: {'description': 'E-mail ou senha icorretos'},
          }
          )
def login(dados: LoginRequest, db:Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.hash_senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha icorreto")
    token = criar_token({"sub": usuario.email, "nome": usuario.nome})
    return {"access_token": token, "token_type": "bearer"}

 
# GET /usuarios - Listar todos 
@app.get("/meu-perfil", response_model=UsuarioResponse,
         tags=['Usuário'],
         summary='Ver meu perfil(requer login)',
         description='Retorna os dados de um usuário autenticado. Requer token JWT válido',
         responses={
              200: {'description': 'Perfil retornado'},
              401: {'description': 'Token ausente ou inválido'},
              404: {'description': 'Usuário não encontrado'},
         }
         ) 
def meu_perfil(email: str = Depends(usuario_logado), db: Session = Depends(get_db)): 
    usuario = db.query(Usuario).filter(Usuario.email == email).first() 
    if not usuario: 
        raise HTTPException(status_code=404, detail="Usuário não encontrado") 
    return usuario 
 
 
 
# GET /usuarios/{id} - Buscar por ID 
@app.get("/usuarios", response_model=List[UsuarioResponse],
         tags=['Usuários'],
         summary='Listar todos usuários',
         description='Retorna a lista de usuários. Rota pública.',
         responses={
              200: {'description': 'Lista retornada com sucesso.'},
         }
         ) 
def listar_usuarios(db: Session = Depends(get_db)): 
    return db.query(Usuario).filter(Usuario.ativo == True).all() 
 
 
# PATCH /usuarios/{id} - Atualizar parcialmente 
@app.patch('/usuarios/{usuario_id}', response_model=UsuarioResponse,
           tags=['Usuários'],
           summary='Atualizar meus dados (requer login)',
           description='Atualiza nome ou e-mail. Só é possível editar o **próprio perfil**',
           responses={
                200: {'description': 'Dados atualizados'},
                401: {'description': 'Não autenticado'},
                403: {'description': 'Sem permissão para editar'},
                404: {'description': 'Usuário não encontrado'},
           }
           )
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
@app.delete('/usuarios/{usuario_id}',
            tags=['Usuários'],
            summary='Desativar conta(requer login)',
            description='Realiza soft delete - a conta é desativa, não é apagada do banco.',
            responses={
                 200: {'description': 'Conta desativada'},
                 404: {'description': 'Usuário não encontrado'},
            }
            ) 
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