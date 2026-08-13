from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso
from logica import calcular_dias_restantes
from pydantic import BaseModel
from datetime import date 

app = FastAPI()
class RecursoCreate(BaseModel):
    nome: str
    intervalo_medio_dias: int
    data_ultima_compra: date
    id_contato: int



Session = sessionmaker(bind=engine)

@app.get("/recursos")
def listar_recursos():
    session = Session()
    recursos = session.query(Recurso).all()
    resultado = [{"ID": r.id, "Nome": r.nome} for r in recursos]
    session.close()
    return resultado

@app.get("/recursos/{nome}")
def detalhe_recurso(nome: str):
    session = Session()
    recurso = session.query(Recurso).filter(Recurso.nome.contains(nome)).first()
    session.close()

    if recurso is None:
        return {"Erro": "Recurso não encontrado"}

    dias = calcular_dias_restantes(recurso)
    return {"nome": recurso.nome, "dias_restantes": dias}


@app.post("/recursos")
def criar_recurso(recurso: RecursoCreate):
    session = Session()
    novo_recurso = Recurso(
        nome=recurso.nome,
        intervalo_medio_dias=recurso.intervalo_medio_dias,
        data_ultima_compra=recurso.data_ultima_compra,
        id_contato=recurso.id_contato
    )

    session.add(novo_recurso)
    session.commit()
    session.refresh(novo_recurso)
    session.close()

    return{"Id": novo_recurso.id, "Nome": novo_recurso.nome, "mensagem": "Recurso criado com sucesso!"  }
