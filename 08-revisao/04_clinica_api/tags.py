from fastapi import APIRouter

# Definição das tags para documentação Swagger
tags_metadata = [
    {
        "name": "Autenticação",
        "description": "Endpoints para registro e login de usuários"
    },
    {
        "name": "Médicos",
        "description": "Gerenciamento de médicos (CRUD)"
    },
    {
        "name": "Pacientes",
        "description": "Gerenciamento de pacientes (CRUD)"
    },
    {
        "name": "Consultas",
        "description": "Gerenciamento de consultas médicas"
    }
]