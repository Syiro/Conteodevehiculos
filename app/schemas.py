from pydantic import BaseModel
from typing import Optional

class configuracion(BaseModel):
    idconfiguracion:Optional[int]
    brillo:int
    contraste:int
    color:int
    modo:str
    redneuronal:str
    skipfps:int
    treshold:float
    
    class Config:
        orm_mode = True
 
class datossemaforo(BaseModel):
    idusuarios:Optional[int]
    idcarros:int
    fecha:str
            
    class Config:
        orm_mode = True
        
        
class datossemaforoUpdate(BaseModel):
    fecha:str
    
    class Config:
        orm_mode = True



class configuracionUpdate(BaseModel):
    modo:str

    class Config:
        orm_mode = True


class Respuesta(BaseModel):
    mensaje:str

    

            