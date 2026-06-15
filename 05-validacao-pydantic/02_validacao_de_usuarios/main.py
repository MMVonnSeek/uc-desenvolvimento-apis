from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models   import Aluno
from schemas  import AlunoCreate, AlunoPatch, AlunoResponse, ErroResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='API de Alunos',
    description='Demonstração de validação avançada com Pydantic',
    version='1.0.0'
)

@app.post('/alunos',
          response_model=AlunoResponse,
          status_code=201,
          responses={409: {'model': ErroResponse}})
def criar_aluno(dados: AlunoCreate, db: Session = Depends(get_db)):

    existe = db.query(Aluno).filter(Aluno.email == dados.email).first()
    if existe:
        raise HTTPException(
            status_code=409,
            detail='E-mail já cadastrado'
        )

    aluno = Aluno(
        nome = dados.nome,
        email = dados.email,
        matricula = dados.matricula,
        nota_final = dados.nota_final,
        ativo=True
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


@app.get('/alunos', response_model=List[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).filter(Aluno.ativo == True).all()

@app.get('/alunos/{aluno_id}', response_model=AlunoResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')
    return aluno

@app.patch('/alunos/{aluno_id}', response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: AlunoPatch,
                       db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')

    if dados.email and dados.email != aluno.email:
        if db.query(Aluno).filter(Aluno.email == dados.email).first():
            raise HTTPException(status_code=409, detail='E-mail já em uso')

    if dados.nome is not None: aluno.nome = dados.nome
    if dados.email is not None: aluno.email = dados.email
    if dados.nota_final is not None: aluno.nota_final = dados.nota_final
    db.commit()
    db.refresh(aluno)
    return aluno

@app.delete('/alunos/{aluno_id}')
def remover_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')
    aluno.ativo = False
    db.commit()
    return {'mensagem': f'Aluno {aluno_id} removido'}