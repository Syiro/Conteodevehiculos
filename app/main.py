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
    datossemaforo = models.datossemaforo(fecha=entrada.fecha, carrosdetectados=entrada.carrosdetectados)
    db.add(datossemaforo)
    db.commit()
    db.refresh(datossemaforo)
    return datossemaforo

@app.put('/datossemaforo/{datossemaforo_id}',response_model=schemas.datossemaforo)
def create_config(idcarros_id:int,entrada:schemas.datossemaforoUpdate,db:Session=Depends(get_db)):
    datossemaforo = db.query(models.datossemaforo).filter_by(idcarros=idcarros_id).first()
    datossemaforo.fecha=entrada.fecha
    db.commit()
    db.refresh(datossemaforo)
    return datossemaforo
 
@app.delete('/datossemaforo/´{datossemaforo_id}',response_model=schemas.Respuesta)
def datossemaforo(idcarros_id:int,db:Session=Depends(get_db)):
    datossemaforo = db.query(models.datossemaforo).filter_by(idcarros=idcarros_id).first()
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
                                         modo= entrada.modo, redneuronal=entrada.redneuronal , skipfps=entrada.skipfps , treshold = entrada.treshold, vmax=entrada.vmax)
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



@app.get('/departamentos/',response_model=List[schemas.departamentos])
def show_config(db:Session=Depends(get_db)):
    departamentos = db.query(models.departamentos).all()
    return departamentos

@app.post('/departamentos/',response_model=schemas.departamentos)
def create_config(entrada:schemas.departamentos,db:Session=Depends(get_db)):
    departamentos = models.departamentos(nombredepartamento= entrada.nombredepartamento)
    db.add(departamentos)
    db.commit()
    db.refresh(departamentos)
    return departamentos

@app.put('/departamentos/{departamentos_id}',response_model=schemas.departamentos)
def create_config(departamentos_id:int,entrada:schemas.departamentosUpdate,db:Session=Depends(get_db)):
    departamentos = db.query(models.departamentos).filter_by(iddepartamentos=departamentos_id).first()
    departamentos.nombredepartamento=entrada.nombredepartamento
    db.commit()
    db.refresh(departamentos)
    return departamentos
 
@app.delete('/departamentos/´{departamentos}',response_model=schemas.Respuesta)
def delete_config(departamentos_id:int,db:Session=Depends(get_db)):
    departamentos = db.query(models.departamentos).filter_by(iddepartamentos=departamentos_id).first()
    db.delete(departamentos)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eleminado exitosamente")
    return respuesta
#METODOS PARA MUNICIPIOS

@app.get('/municipios/',response_model=List[schemas.municipios])
def show_config(db:Session=Depends(get_db)):
    municipios = db.query(models.municipios).all()
    return municipios

@app.post('/municipios/',response_model=schemas.municipios)
def create_config(entrada:schemas.municipios,db:Session=Depends(get_db)):
    municipios= models.municipios(nombremunicipio = entrada.nombremunicipio)
    db.add(municipios)
    db.commit()
    db.refresh(municipios)
    return municipios
@app.put('/municipios/{municipios_id}',response_model=schemas.municipios)
def create_config(municipios_id:int,entrada:schemas.municipiosUpdate,db:Session=Depends(get_db)):
    municipios = db.query(models.municipios).filter_by(idmunicipios=municipios_id).first()
    municipios.nombremunicipio=entrada.nombremunicipio
    db.commit()
    db.refresh(municipios)   
    return municipios
 
@app.delete('/municipios/´{municipios_id}',response_model=schemas.Respuesta)
def delete_config(municipios_id:int,db:Session=Depends(get_db)):
    municipios = db.query(models.municipios).filter_by(idmunicipios=municipios_id).first()
    db.delete(municipios)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eleminado exitosamente")
    return respuesta


#USUARIOS

@app.get('/usuarios/',response_model=List[schemas.usuarios])
def show_config(db:Session=Depends(get_db)):
    usuarios = db.query(models.usuarios).all()
    return usuarios

@app.post('/usuarios/',response_model=schemas.usuarios)
def create_config(entrada:schemas.usuarios,db:Session=Depends(get_db)):
    usuarios = models.usuarios(nombre=entrada.nombre,telefono=entrada.telefono,mail=entrada.mail)
    db.add(usuarios)
    db.commit()
    db.refresh(usuarios)
    return usuarios

@app.put('/usuarios/{usuarios_id}',response_model=schemas.usuarios)
def create_config(usuarios_id:int,entrada:schemas.usuariosUpdate,db:Session=Depends(get_db)):
    usuarios = db.query(models.usuarios).filter_by(idusuarios=usuarios_id).first()
    usuarios.nombre=entrada.nombre
    db.commit()
    db.refresh(usuarios)
    return usuarios
 
@app.delete('/usuarios/´{usuarios_id}',response_model=schemas.Respuesta)
def delete_config(usuarios_id:int,db:Session=Depends(get_db)):
    usuarios = db.query(models.usuarios).filter_by(idusuarios=usuarios_id).first()
    db.delete(usuarios)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eleminado exitosamente")
    return respuesta
