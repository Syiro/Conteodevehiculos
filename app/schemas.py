from pydantic import BaseModel
from typing import Optional

class configuracion(BaseModel):
    idconfiguracion:int
    brillo:int
    contraste:int
    color:int
    modo:str
    redneuronal:str
    
    class Config:
        orm_mode = True
            