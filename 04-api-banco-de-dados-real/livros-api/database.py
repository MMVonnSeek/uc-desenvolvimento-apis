from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco - SQLite salva em um arquivo banco.db na pasta do projeto 
DATABASE_URL = 'sqlite:///./banco.db'

# Engine: motor de conexão com o banco
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)

# SessionaLocal: fábrica de sessões - cada requisição tem a sua
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

# Base: classe base que todos os modelos vão herdar
Base = declarative_base()

# yield encerra a sessão
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()