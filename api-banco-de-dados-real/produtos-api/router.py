from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import list

from database import get_db
from models import Produto
from schemas import ProdutoCreate,ProdutoPatch, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get('/', response_model=list[ProdutoResponse])
def listar_produto(skip: int = 0, limit: int = 10,db: Session = Depends(get_db)):
    return db.query(Produto).filter(Produto.ativo == True).offset(skip).limit(limit).all()

@router.get('/{produto_id}', response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post('/', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@router.put('/{produto_id}', response_model=ProdutoResponse)
def substituir_produto(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.estoque = dados.estoque
    db.commit()
    db.refresh(produto)
    return produto

@router.patch('/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoPatch, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if dados.nome is not None: produto.nome = dados.nome
    if dados.preco is not None: produto.preco = dados.preco
    if dados.estoque is not None: produto.estoque = dados.estoque
    db.commit()
    db.refresh(produto)
    return produto

@router.delete('/{produto_id}', status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto.ativo = False
    db.commit()
    return{'mensagem': f'Produto {produto_id} desativado'}