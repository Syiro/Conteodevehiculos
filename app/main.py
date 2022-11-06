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
    configuracion = db.query(models.configuracion.all())
    return configuracion


