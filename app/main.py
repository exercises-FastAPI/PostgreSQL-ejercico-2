from typing import List
from fastapi import FastAPI, Request
from fastapi.params import Depends
from starlette.responses import RedirectResponse
import models,schemas
from conexion import SessionLocal,engine
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import json
from fastapi.encoders import jsonable_encoder
from starlette.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory='../templates')
app.mount("/iconfont", StaticFiles(directory="../iconfont"), name="iconfont")
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/js", StaticFiles(directory="../js"), name="js")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/', response_model=List[schemas.User])
def show_users(request: Request, db:Session=Depends(get_db)):
    usuarios = db.query(models.User).all()
    json_datos = jsonable_encoder(usuarios)
    return templates.TemplateResponse('index.html', {'request': request, 'listado': json_datos})

@app.get('/obtener/{usuario_id}', response_model=List[schemas.User])
def get_users(request: Request, usuario_id:int, db:Session=Depends(get_db)):
    usuarios = db.query(models.User).get(usuario_id)
    json_datos = jsonable_encoder(usuarios)
    return templates.TemplateResponse('home.html', {'request': request, 'datos': json_datos})

@app.post('/add_user/', response_model=schemas.User)
async def create_users(request: Request, db:Session=Depends(get_db)):
    form_data = await request.form()
    nombre = form_data['nombre']
    edad = form_data['edad']
    direccion = form_data['direccion']
    correo = form_data['correo']
    usuario = models.User(nombre = nombre, edad = edad, direccion = direccion, correo = correo)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return RedirectResponse("/",303)  

@app.post('/update_user', response_model=schemas.User)
async def update_users(request:Request, db:Session=Depends(get_db)):
    form_data = await request.form()
    usuario_id = form_data['usuario_id']
    nombre = form_data['u_nombre']
    edad = form_data['u_edad']
    direccion = form_data['u_direccion']
    correo = form_data['u_correo']    
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    usuario.nombre = nombre
    usuario.edad = edad
    usuario.direccion = direccion
    usuario.correo = correo
    db.commit()
    db.refresh(usuario)
    return RedirectResponse("/",303)  

@app.get('/eliminar/{usuario_id}', response_model=schemas.Respuesta)
def delete_users(request:Request, usuario_id:int, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return RedirectResponse('/', 303)