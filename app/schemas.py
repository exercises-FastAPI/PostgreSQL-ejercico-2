from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id:Optional[int]
    nombre:str
    edad:int
    direccion:str
    correo:str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nombre:str
    edad:int
    direccion:str
    correo:str

    class Config:
        orm_mode = True

class Respuesta(BaseModel):
    mensaje:str