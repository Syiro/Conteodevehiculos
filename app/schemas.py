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
        
class configuracionUpdate(BaseModel):
    modo:str
    class Config:
        orm_mode = True        
 
class datossemaforo(BaseModel):
    idcarros:Optional[int]
    fecha:str
    carrosdetectados:int
            
    class Config:
        orm_mode = True
              
class datossemaforoUpdate(BaseModel):
    fecha:str
    
    class Config:
        orm_mode = True

class departamentos(BaseModel):
    iddepartamentos:Optional[int]
    nombredepartamento:str
    
    class Config:
        orm_mode = True
        
class departamentosUpdate(BaseModel):
    nombredepartamento:str 
    
    class Config:
        orm_mode = True       
    
class municipios(BaseModel):
    idmunicipios:Optional[int]
    nombremunicipio:str

    class Config:
        orm_mode = True

class municipiosUpdate(BaseModel):
    nombremunicipio:str
    
    class Config:
        orm_mode=True

class usuarios(BaseModel):
    nombre : str
    telefono : str
    mail : str
    
    class Config:
        orm_mode=True
        
class usuariosUpdate(BaseModel):
    nombre:str
    class Config:
        orm_mode=True

class Respuesta(BaseModel):
    mensaje:str

    

            