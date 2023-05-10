from sqlalchemy import Column, Integer, String , Float, ForeignKey, Date
from app.Conexion import Base

class configuracion(Base):
    __tablename__='configuracion'
    idconfiguracion = Column(Integer, primary_key=True)
    idusuarios = Column(Integer, ForeignKey("usuarios.idusuarios"))
    idmunicipios = Column(Integer, ForeignKey("municipios.idmunicipios"))
    brillo = Column(Integer)
    contraste = Column(Integer)
    color = Column(Integer)
    modo = Column(String(45))
    redneuronal = Column(String(45))
    skipfps = Column(Integer)
    treshold = Column(Float)
    vmax = Column(Integer)
    
class datossemaforo(Base):
    __tablename__='datossemaforo'
    idcarros = Column(Integer, primary_key=True)
    idusuarios = Column(Integer, ForeignKey("usuarios.idusuarios"))
    fecha = Column(String(45))
    carrosdetectados = Column(Integer)
    

class departamentos(Base):
    __tablename__='departamentos'
    iddepartamentos = Column(Integer, primary_key=True)
    idconfiguracion = Column(Integer)
    idmunicipios = Column(Integer)
    nombredepartamento = Column(String(255))
    
class municipios(Base):
    __tablename__='municipios'
    idmunicipios = Column(Integer, primary_key=True)
    iddepartamentos = Column(Integer, ForeignKey("departamentos.iddepartamentos"))
    nombremunicipio = Column(String(255))

class usuarios(Base):
    __tablename__='usuarios'
    idusuarios = Column(Integer, primary_key=True)       
    nombre = Column((String(45)))
    telefono = Column((String(45)))
    mail = Column(String(255))