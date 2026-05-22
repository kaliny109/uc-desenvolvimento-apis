from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models   import Usuario
from schemas  import UsuarioCreate, UsuarioPatch, UsuarioResponse, ErroResponse

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API funcionando"}

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='API de Alunos',
    description='Demonstração de validação avançada com Pydantic',
    version='1.0.0'
)
# POST /usuarios - Cadastrar novo usuário
# response_model=UsuarioResponse garante que a senha NUNCA vai
# aparecer na resposta, mesmo que o objeto Usuario tenha hash_senha.
@app.post('/usuarios',
          response_model=UsuarioResponse,
          status_code=201,
          responses={409: {'model': ErroResponse}})
def criar_aluno(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica email duplicado antes de tentar inserir
    existe = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existe:
        raise HTTPException(
            status_code=409,
            detail='E-mail já cadastrado'
        )
    # Em produção: hash_senha = bcrypt.hashpw(dados.senha...)
    # Por enquanto guardamos a senha diretamente só para estudar o schema
    # (no Capítulo 6 implementamos o bcrypt de verdade)
    aluno = Usuario(
        nome = dados.nome,
        email = dados.email,
        matricula = dados.matricula,
        nota_final = dados.nota_final,
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno   # FastAPI filtra pela UsuarioResponse — sem senha!


# GET /alunos - Listar todos
@app.get('/alunos', response_model=List[UsuarioResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.ativo == True).all()


# GET /alunos/{id} - Buscar por ID
@app.get('/alunos/{aluno_id}', response_model=UsuarioResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).filter(Usuario.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')
    return aluno


# PATCH /alunos/{id} - Atualizar parcialmente
@app.patch('/alunos/{aluno_id}', response_model=UsuarioResponse)
def atualizar_aluno(aluno_id: int, dados: UsuarioPatch,
                       db: Session = Depends(get_db)):
    aluno = db.query(Usuario).filter(Usuario.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')

    # Verifica email duplicado se o cliente quiser mudar o email
    if dados.email and dados.email != aluno.email:
        if db.query(Usuario).filter(Usuario.email == dados.email).first():
            raise HTTPException(status_code=409, detail='E-mail já em uso')

    if dados.nome  is not None: aluno.nome  = dados.nome
    if dados.email is not None: aluno.email = dados.email
    db.commit()
    db.refresh(aluno)
    return aluno


# DELETE /alunos/{id} - Soft delete
@app.delete('/alunos/{aluno_id}')
def remover_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).filter(Usuario.id == aluno_id).first()
    if not aluno or not aluno.ativo:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')
    aluno.ativo = False
    db.commit()
    return {'mensagem': f'Aluno {aluno_id} removido'}