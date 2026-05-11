from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI (title='API de Filmes', version='1.0.0')

# Banco de dados em memória (lista Python)
# Em produção: usariamos SQlite, PostgreSQL, etc...
Filmes = [
    {"id": 1, "nome": "10 coisas que eu odeio em você", "genero": "romance", "duração": 190},
    {"id": 2, "nome": "Legalmente Loira", "genero": "comédia", "duração": 120},
    {"id": 3, "nome": "Superman", "genero": "ação", "duração": 195}
]
proximo_id = 4 # Controlar o próximo iD

class FilmeCreate(BaseModel):
    nome: str
    genero: str
    duração: int

# GET /filmes -> lista todos os filmes
@app.get('/filmes')
def listar_filmes():
    return Filmes

# GET /filmes/(id) -> busca um filme pelo ID
@app.get('/filmes/{filme_id}')
def buscar_filme(filme_id: int):
    filme = next(
        (f for f in Filmes if f['id'] == filme_id),
        None # valor padrao se não encontrar
    )   
    if filme is None:
        return {"erro": f"Filme {filme_id} não encontrado"}
    return filme

# POST /filmes -> cria um novo filme
@app.post('/filmes', status_code=201)
def criar_filme(filme: FilmeCreate):
    global proximo_id

    novo_filme = {
        'id': proximo_id,
        'nome': filme.nome,
        'genero': filme.genero,
        'duração': filme.duração,
    }

    Filmes.append(novo_filme)
    proximo_id += 1

    return novo_filme


