from sqlalchemy import Column, Integer, String
from app.Conexion import Base

class configuracion(Base):
    __tablename__='configuracion'
    idconfiguracion = Column(Integer, primary_key=True)
    #idusuarios = Column(Integer, forean_key=True)
    #idmunicipios = Column(Integer, forean_key=True)
    brillo = Column(Integer)
    contraste = Column(Integer)
    color = Column(Integer)
    modo = Column(String(45))
    redneuronal = Column(String(45))