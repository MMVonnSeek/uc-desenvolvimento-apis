# API de Pagamentos - E-commerce SENAI

API REST completa para gerenciamento de um e-commerce com sistema de pagamentos, desenvolvida como projeto final do curso de Desenvolvimento de APIs com FastAPI.

## Descrição

Esta API simula o back-end de uma loja virtual moderna, permitindo:

- Cadastro e autenticação de usuários (JWT)
- Gerenciamento de produtos (CRUD com controle de estoque)
- Criação e gestão de pedidos de compra
- Processamento de pagamentos com múltiplos métodos
- Controle de estoque automático
- Documentação interativa via Swagger

## Tecnologias

| Tecnologia | Versão  | Descrição                        |
| ---------- | ------- | -------------------------------- |
| Python     | 3.10+   | Linguagem principal              |
| FastAPI    | 0.104.1 | Framework web                    |
| SQLAlchemy | 2.0.23  | ORM para banco de dados          |
| SQLite     | -       | Banco de dados (desenvolvimento) |
| Pydantic   | 2.5.0   | Validação de dados               |
| JWT        | 3.3.0   | Autenticação                     |
| bcrypt     | 1.7.4   | Hash de senhas                   |

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/mmvonnseek/uc-desenvolvimento-apis.git
cd uc-desenvolvimento-apis/09-projeto-final

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com sua SECRET_KEY

# 5. Execute a API
uvicorn main:app --reload

# 6. Acesse a documentação
# Abra o navegador em: http://127.0.0.1:8000/docs
```
