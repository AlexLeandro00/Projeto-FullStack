from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso
from logica import calcular_dias_restantes
from pydantic import BaseModel
from datetime import date 
from typing import Optional

app = FastAPI()
class RecursoCreate(BaseModel):
    nome: str
    intervalo_medio_dias: int
    data_ultima_compra: date
    id_contato: int

class RecursoUpdate(BaseModel):
    nome: Optional[str] = None
    intervalo_medio_dias: Optional[int] = None
    data_ultima_compra: Optional[date] = None
    id_contato: Optional[int] = None



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
    recurso = session.query(Recurso).filter(Recurso.nome.ilike(f"%{nome}%")).first()
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




@app.patch("/recursos/{id_recurso}")
def atualizar_recurso(id_recurso: int, dados: RecursoUpdate):
    session = Session()
    recurso = session.query(Recurso).filter(Recurso.id == id_recurso).first()

    if recurso is None:
        session.close()
        return {"Erro": "Recurso não encontrado"}

    if dados.nome is not None:
        recurso.nome = dados.nome
    if dados.intervalo_medio_dias is not None:
        recurso.intervalo_medio_dias = dados.intervalo_medio_dias
    if dados.data_ultima_compra is not None:
        recurso.data_ultima_compra = dados.data_ultima_compra
    if dados.id_contato is not None:
        recurso.id_contato = dados.id_contato

    session.commit()
    session.refresh(recurso)
    session.close()
    return {"Id": recurso.id, "Nome": recurso.nome, "mensagem": "Recurso atualizado com sucesso!"}


@app.delete("/recursos/{id_recurso}")
def deletar_recurso(id_recurso: int):
    session = Session()
    recurso = session.query(Recurso).filter(Recurso.id == id_recurso).first()

    if recurso is None:
        session.close()
        return {"Erro": "Recurso não encontrado"}

    session.delete(recurso)
    session.commit()
    session.close()

    return {"mensagem": f"Recurso {recurso.nome} deletado com sucesso!"}