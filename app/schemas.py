from pydantic import BaseModel
from typing import Optional

class configuracion(BaseModel):
    idconfiguracion:Optional[int]
    brillo:int
    contraste:int
    color:int
    modo:str
    redneuronal:str
    
    class Config:
        orm_mode = True

class configuracionUpdate(BaseModel):
    modo:str

    
    class Config:
        orm_mode = True

class Respuesta(BaseModel):
    mensaje:str

    

            