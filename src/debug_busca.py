from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso

session = sessionmaker(bind=engine)()

todos = session.query(Recurso).all()
for r in todos:
    print(repr(r.nome))

session.close()