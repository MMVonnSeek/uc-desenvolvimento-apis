# Aula 01 - Introdução a APIs


## O que aprendemos hoje

- [x] O que é uma API (analogia do garçom)
- [x] O que é JSON
- [x] Como consumir uma API com fetch()
- [x] Método HTTP GET
- [x] Status Code (200, 404)
- [x] Estrutura de Requisição e Resposta HTTP

## APIs utilizadas

| API | URL | Documentação |
|-----|-----|--------------|
| The Cat API | `https://api.thecatapi.com/v1/images/search` | [docs](https://developers.thecatapi.com) |
| GitHub API | `https://api.github.com/users/${nome}` | [docs](https://docs.github.com/en/rest/users/users?apiVersion=2026-03-10#get-a-user) |

## Atividades

### 🎓 Atividade Guiada: Cat API
Criamos juntos uma página que mostra gatos aleatórios.

**Conceitos aplicados:** fetch(), .then(), .json(), manipulação do DOM

[Ver código](./cat-api/)

### ✏️ Exercício: GitHub API
Desafio individual: adaptar o código para consumir a API do GitHub.

**Diferencial:** A resposta da API do GitHub é um objeto JSON direto, diferente da Cat API que retorna um array.

**Exemplo de campos úteis:**

- login (nome do usuário)

- avatar_url (foto)

- public_repos (quantidade de repositórios)

[Ver código](./github-api/)

## Comandos importantes

``` 
fetch('url')          // Faz a requisição HTTP
  .then(r => r.json()) // Converte resposta para JSON
  .then(d => usar(d))  // Usa os dados recebidos
```
