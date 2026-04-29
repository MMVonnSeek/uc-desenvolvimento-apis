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
| Dog API | `https://dog.ceo/api/breeds/image/random` | [docs](https://dog.ceo/dog-api/) |

## Atividades

### 🎓 Atividade Guiada: Cat API
Criamos juntos uma página que mostra gatos aleatórios.

**Conceitos aplicados:** fetch(), .then(), .json(), manipulação do DOM

[Ver código](./cat-api/)

### ✏️ Exercício: Dog API
Desafio individual: adaptar o código para consumir a Dog API.

**Diferencial:** O JSON da Dog API tem estrutura diferente (dados.message vs dados[0].url)

[Ver código](./exercicio-dog-api/)

## Comandos importantes

``` 
fetch('url')          // Faz a requisição HTTP
  .then(r => r.json()) // Converte resposta para JSON
  .then(d => usar(d))  // Usa os dados recebidos
```
