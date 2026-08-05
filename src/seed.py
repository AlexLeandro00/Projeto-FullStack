from sqlalchemy.orm import sessionmaker
from database import engine
from models import Contato, Recurso
from datetime import date


Session = sessionmaker(bind=engine)
session = Session()


contato_agua = Contato(nome="Água Cristal LTDA", telefone="(81) 99999-9999")
session.add(contato_agua)
session.commit()

recurso_agua = Recurso(
    nome="Água Mineral",
    intervalo_medio_dias=7,
    data_ultima_compra=date(2026, 8, 5),
    contato=contato_agua
)
session.add(recurso_agua)
session.commit()

print("Dados de teste inseridos com sucesso!")
session.close()
