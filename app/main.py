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

@app.get('/configuracion/',response_model=List[schemas.configuracion])
def show_config(db:Session=Depends(get_db)):
    configuracion = db.query(models.configuracion).all()
    return configuracion

@app.post('/configuracion/',response_model=schemas.configuracion)
def create_config(entrada:schemas.configuracion,db:Session=Depends(get_db)):
    configuracion = models.configuracion(brillo = entrada.brillo, contraste = entrada.contraste, color = entrada.color, 
                                         modo= entrada.modo, redneuronal=entrada.redneuronal)
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
 

