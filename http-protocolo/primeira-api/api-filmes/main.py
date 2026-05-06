from fastapi import FastAPI

app = FastAPI(
    title="Minha Primeira API",
    description="Criada no SENAI por: kaliny com FastAPI",
    version="1.0.0"
)
#GET /sobre informaçoes sobre a API
@app.get('/sobre')
def raiz():
    return {
        "api": "Minha Primeira API", 
        "versão": "1.0.0",
        "framework": "FastAPI",
        "linguagem": "Python 3",
        "escola": "SENAI"
    }
    
@app.get('/saudacao/{nome}')
def saudar(nome: str):
    return {
    "mensagem": f"Olá, {nome}! Seja bem-vindo à minha API!",
    "nome_recebido": nome
    }
    