from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso
from logica import calcular_dias_restantes

Session = sessionmaker(bind=engine)
session = Session()

recurso = session.query(Recurso).filter(Recurso.nome.contains("Mineral")).first()
dias = calcular_dias_restantes(recurso)

print(f"Faltam {dias} dias para acabar a água.")

session.close()