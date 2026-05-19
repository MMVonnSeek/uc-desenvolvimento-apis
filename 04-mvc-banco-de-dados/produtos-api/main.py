from fastapi import FastAPI
from database import engine, Base
from router import router as produto_router

# Cria as tabelas no banco ao iniciar a API
# Se o banco.db não existir, cria o arquivo e as tabelas
# Se já existir, não faz nada - não apaga os dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Produtos",
    description="CRUD com FastAPI + SQLAlchemy + SQlite",
    version="2.0.0"
)

# Registra o router com prefixo /produtos
app.include_router(produto_router)

@app.get('/')
def raiz():
    return {"status": "online", "docs": "/docs", "versao": "2.0.0"}