from fastapi import FastAPI
from database import engine, Base
from router import router as livros_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livros",
    description="CRUD com FastAPI e SQLAlchemy",
    version="2.0.0"
)

app.include_router(livros_router)

@app.get('/')
def raiz():
    return {'status': "online", "docs": "/docs", "version": "2.0.0"}