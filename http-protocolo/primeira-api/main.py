from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI (title='API de Produtos', version='1.0.0')

# Banco de dados em memoria (lista Python)
# Em produção: usariamos SQlite, PostgreSQL, etc...
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3499.99, "estoque": 10},
    {"id": 2, "nome": "Mouse", "preco": 90.00, "estoque": 50},
    {"id": 3, "nome": "Teclado", "preco": 120.00, "estoque": 30}
]
proximo_id = 4

class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    estoque: int = 0

@app.get('/produtos')    
def listar_produtos():
    return produtos

@app.get('/produtos/{produto_id}')
def buscar_produto(produto_id: int):
    produto = next(
        (p for p in produtos if p[id] == produto_id),
        None
    )
    if produto is None:
      return {"erro": f"Produto {produto_id} não encontrado"}
    return produto   

@app.post('/produtos', status_code=201)
def criar_produto(produto: ProdutoCreate):
    global proximo_id

    novo_produto = {
        'id': proximo_id,
        'nome': produto.nome,
        'preco': produto.preco,
        'estoque': produto.estoque,
    } 
    produtos.append(novo_produto)
    proximo_id += 1

    return novo_produto