from sqlalchemy import create_engine
from models import Base

engine = create_engine('sqlite:///gestor.db')

def cria_banco():
    Base.metadata.create_all(engine)
    print("Banco de dados criado com sucesso!")


if __name__ == "__main__":
    cria_banco()
    