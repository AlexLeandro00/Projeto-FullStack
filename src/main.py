from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso
from logica import calcular_dias_restantes

app = FastAPI()
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
