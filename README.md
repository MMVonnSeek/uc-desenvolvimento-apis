# 🏗️ Em construção...
# UC — Desenvolvimento de APIs
![Curso](https://img.shields.io/badge/curso-Técnico%20em%20Informática%20para%20Internet-blue)
![Instituição](https://img.shields.io/badge/instituição-SENAI-red)
![UC](https://img.shields.io/badge/UC-Desenvolvimento%20de%20APIs-green)
![Professor](https://img.shields.io/badge/professor-Max%20Muller-orange)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
 
## Sobre esta UC
 
Nesta Unidade Curricular aprendemos a criar e consumir **APIs REST** utilizando **Python** e **FastAPI**, seguindo boas práticas de mercado: validação com Pydantic, banco de dados com SQLAlchemy, autenticação JWT e documentação automática via Swagger.
 
<div align="center">
  <img src="screenshots/image-api.png" alt="Exemplo de API FastAPI com Swagger UI" width="800">
</div>
 
## Planejamento das Aulas
 
| # | Tema | Conteúdo | Exemplo Guiado | Exercício | Status |
|:-:|------|----------|:--------------:|:---------:|:------:|
| 1 | **Introdução a APIs** | Conceito, JSON, fetch(), analogia do garçom | Cat API no navegador | Github API | ✅ |
| 2 | **HTTP + Primeira API** | Protocolo HTTP, métodos, status codes, FastAPI básico | Primeira API FastAPI | API de Filmes | ⏳ |
| 3 | **CRUD Completo** | GET, POST, PUT, PATCH, DELETE, HTTPException | CRUD de Produtos | CRUD de Tarefas | ⏳ |
| 4 | **MVC + Banco de Dados** | SQLAlchemy, ORM, Depends(), estrutura MVC | Produtos API + SQLite | Livros API + SQLite | ⏳ |
| 5 | **Validação com Pydantic** | BaseModel, Field, validators, schemas de entrada/saída | Schemas avançados | Validação de Usuários | ⏳ |
| 6 | **Autenticação JWT** | bcrypt, JWT, registro, login, proteção de rotas | Auth API Completa | Tarefas com Auth | ⏳ |
| 7 | **Documentação Swagger** | summary, description, exemplos, tags | Docs ricos na API | Biblioteca documentada | ⏳ |
| 8 | **Projeto Final** | Sistema completo com todos os conteúdos da UC | — | API completa | 🔒 |
 
> **Legenda:** ✅ Concluída · ⏳ Em andamento · 🔒 Aguardando
 
---
 
## Objetivos de Aprendizagem
 
Ao final desta UC, o aluno deverá ser capaz de:
 
- [x] Compreender o conceito de API e sua importância no desenvolvimento moderno
- [x] Consumir APIs externas utilizando `fetch()` no JavaScript
- [ ] Entender o protocolo HTTP (requisição, resposta, métodos, status codes)
- [ ] Criar APIs REST com Python e FastAPI
- [ ] Implementar endpoints REST completos (GET, POST, PUT, PATCH, DELETE)
- [ ] Validar dados de entrada com Pydantic
- [ ] Conectar uma API a um banco de dados SQLite com SQLAlchemy
- [ ] Organizar projetos no padrão MVC
- [ ] Implementar autenticação com JWT (JSON Web Tokens)
- [ ] Documentar APIs com Swagger/OpenAPI
- [ ] Aplicar os pilares da segurança da informação (CID) em APIs
 
---
 
## Tecnologias Utilizadas
 
| Tecnologia | Descrição |
|------------|-----------|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | Linguagem principal do back-end |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) | Framework para criação de APIs REST |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white) | Banco de dados relacional local |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=python&logoColor=white) | ORM para comunicação com o banco |
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=python&logoColor=white) | Validação de dados de entrada/saída |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black) | Consumo de APIs no front-end (fetch) |
| ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white) | Controle de versão |
| ![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white) | Hospedagem do repositório |
 
---
 
## Como executar os projetos
 
### Pré-requisitos
 
- Python 3.10 ou superior
- VS Code com extensão Python
- Git instalado
### Passos
 
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/UC-Desenvolvimento-de-APIs.git
cd UC-Desenvolvimento-de-APIs
 
# 2. Acesse a pasta da aula desejada
cd primeira-api/produtos-api
 
# 3. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
 
# 4. Instale as dependências
pip install -r requirements.txt
 
# 5. Execute a API
uvicorn main:app --reload
 
# 6. Acesse a documentação automática
# http://127.0.0.1:8000/docs
```
 
---
 
## Links Úteis
 
### Documentações Oficiais
- [FastAPI](https://fastapi.tiangolo.com/pt/) — documentação oficial em português
- [Pydantic v2](https://docs.pydantic.dev/) — validação de dados
- [SQLAlchemy](https://docs.sqlalchemy.org/) — ORM para banco de dados
- [MDN Web Docs — HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP) — protocolo HTTP
- [JWT.io](https://jwt.io/) — debugger de tokens JWT
### APIs Públicas para Praticar
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — API fake para testes
- [Public APIs](https://publicapis.dev/) — diretório de APIs públicas gratuitas
### Ferramentas
- [Thunder Client](https://www.thunderclient.com/) — extensão VS Code para testar APIs
- [Insomnia](https://insomnia.rest/) — cliente REST completo
- [JSON Formatter](https://jsonformatter.org/json-parser) — visualizar JSON formatado
- [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer) — extensão VS Code para visualizar o banco
---
 
## Estratégias Pedagógicas
 
- Aulas 100% práticas com código digitado ao vivo no projetor
- Progressão natural: **consumir API → entender HTTP → criar API**
- Exemplo guiado + exercício de fixação em toda aula
- Projeto único e incremental: cada aula evolui o mesmo repositório
- Uso do Swagger UI como ferramenta de teste integrada
- Versionamento com Git desde a primeira aula
---
 
## Como contribuir
 
- Encontrou um erro no código? Abra uma **Issue**
- Tem uma sugestão de melhoria? Envie um **Pull Request**
- Dúvidas? Use a aba **Discussions**

---

<div align="center">

**Material produzido com ❤️ para os alunos do SENAI**

*"Ensinar não é transferir conhecimento, mas criar as possibilidades para a sua própria produção ou a sua construção."* — Paulo Freire

</div>

---
## Licença
Este repositório contém material didático.

---
<div align="center">
 
[![Stars](https://img.shields.io/github/stars/MMVonnSeek/uc-desenvolvimento-apis?style=social)](https://github.com/MMVonnSeek/uc-desenvolvimento-apis/stargazers)
[![Forks](https://img.shields.io/github/forks/MMVonnSeek/uc-desenvolvimento-apis?style=social)](https://github.com/MMVonnSeek/uc-desenvolvimento-apis/network/members)
[![Follow](https://img.shields.io/github/followers/MMVonnSeek?style=social)](https://github.com/MMVonnSeek)

<a href="https://wa.me/5561986194426?text=Olá%20tudo%20bem%20Max%3F%20Eu%20vim%20pelo%20seu%20repositorio%20do%20github.%20Podemos%20conversar%20sobre%3F" target="_blank">
  <img src="https://img.shields.io/badge/WhatsApp-Fale%20Comigo-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />
</a>

<br>

  [Voltar ao topo](#-uc-desenvolvimento-apis)

</div>
