from sqlalchemy import Column, Integer, String
from conexion import Base

class User(Base):
    __tablename__='usuario'
    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String(50))
    edad = Column(Integer)
    direccion = Column(String(100))
    correo = Column(String(30))