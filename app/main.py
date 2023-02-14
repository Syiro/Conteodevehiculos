from typing import List
from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from fastapi.params import Depends
from app import models
from app import schemas
from app.Conexion import SessionLocal,engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

#METODOS DATOS SEMAFORO

@app.get('/datossemaforo/',response_model=List[schemas.datossemaforo])
def show_config(db:Session=Depends(get_db)):
    datossemaforo = db.query(models.datossemaforo).all()
    return datossemaforo

@app.post('/datossemaforo/',response_model=schemas.datossemaforo)
def create_config(entrada:schemas.datossemaforo,db:Session=Depends(get_db)):
    datossemaforo = models.datossemaforo(idusuarios=entrada.idusuarios, idcarros=entrada.idcarros,fecha=entrada.fecha)
    db.add(datossemaforo)
    db.commit()
    db.refresh(datossemaforo)
    return datossemaforo

@app.put('/datossemaforo/{datossemaforo_id}',response_model=schemas.datossemaforo)
def create_config(datossemaforo_id:int,entrada:schemas.datossemaforoUpdate,db:Session=Depends(get_db)):
    datossemaforo = db.query(models.datossemaforo).filter_by(idusuarios=datossemaforo_id).first()
    datossemaforo.fecha=entrada.fecha
    db.commit()
    db.refresh(datossemaforo)
    return datossemaforo
 
@app.delete('/datossemaforo/´{datossemaforo_id}',response_model=schemas.Respuesta)
def datossemaforo(datossemaforo_id:int,db:Session=Depends(get_db)):
    datossemaforo = db.query(models.datossemaforo).filter_by(idusuarios=datossemaforo_id).first()
    db.delete(datossemaforo)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eleminado exitosamente")
    return respuesta


#METODOS PARA CONFIGURACION

@app.get('/configuracion/',response_model=List[schemas.configuracion])
def show_config(db:Session=Depends(get_db)):
    configuracion = db.query(models.configuracion).all()
    return configuracion

@app.post('/configuracion/',response_model=schemas.configuracion)
def create_config(entrada:schemas.configuracion,db:Session=Depends(get_db)):
    configuracion = models.configuracion(brillo = entrada.brillo, contraste = entrada.contraste, color = entrada.color, 
                                         modo= entrada.modo, redneuronal=entrada.redneuronal , skipfps=entrada.skipfps , treshold = entrada.treshold)
    db.add(configuracion)
    db.commit()
    db.refresh(configuracion)
    return configuracion

@app.put('/configuracion/{configuracion_id}',response_model=schemas.configuracion)
def create_config(configuracion_id:int,entrada:schemas.configuracionUpdate,db:Session=Depends(get_db)):
    configuracion = db.query(models.configuracion).filter_by(idconfiguracion=configuracion_id).first()
    configuracion.modo=entrada.modo
    db.commit()
    db.refresh(configuracion)
    return configuracion
 
@app.delete('/configuracion/´{configuracion_id}',response_model=schemas.Respuesta)
def delete_config(configuracion_id:int,db:Session=Depends(get_db)):
    configuracion = db.query(models.configuracion).filter_by(idconfiguracion=configuracion_id).first()
    db.delete(configuracion)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eleminado exitosamente")
    return respuesta
 
#METODOS PARA DEPARTAMENTOS

#METODOS PARA MUNICIPIOS

#USUARIOS
