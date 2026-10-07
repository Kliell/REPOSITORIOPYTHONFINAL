from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base


class Tutor(Base):
    __tablename__ = 'tutores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True)

    def __repr__(self):
        return f'<Tutor id={self.id} nome={self.nome_completo}>'
   
class Animal(Base):
    __tablename__ = 'animais'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    nome_animal = Column(String(60), nullable=True)
    especie = Column(String(40), nullable=True)
    raca = Column(String(60), nullable=False)
    peso_kg = Column(Float, nullable=True)
    tutor_id = Column(Integer, ForeignKey("tutores.id"))

    def __repr__(self):
        return f'<Animal id={self.id} nome={self.nome_animal}>'

class Atendimento(Base):
    __tablename__ = 'atendimentos'

    id = Column(Integer, primary_key= True, autoincrement= True)
    data_atend = Column(String(10), nullable=True)
    motivo = Column(String(200), nullable=True)
    valor_cons = Column(Float)
    animal_id = Column(Integer, ForeignKey("animais.id"))

