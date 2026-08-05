from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Contato(Base):
    __tablename__ = 'contatos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)



class Recurso(Base):
    __tablename__ = 'recursos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    intervalo_medio_dias = Column(Integer, nullable=False)
    data_ultima_compra = Column(Date, nullable=False)
    id_contato = Column(Integer, ForeignKey('contatos.id'))
    contato = relationship('Contato', backref='recursos')
    