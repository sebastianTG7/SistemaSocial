from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db_config import Base

# Modelos de Catálogo (Tablas Maestras)
class CatTipoUsuario(Base):
    __tablename__ = "cat_tipos_usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    
    personas = relationship("Persona", back_populates="tipo_usuario")

class CatFacultad(Base):
    __tablename__ = "cat_facultades"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    
    escuelas = relationship("CatEscuela", back_populates="facultad")
    personas = relationship("Persona", back_populates="facultad")

class CatEscuela(Base):
    __tablename__ = "cat_escuelas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    facultad_id = Column(Integer, ForeignKey("cat_facultades.id"))
    activo = Column(Boolean, default=True)
    
    facultad = relationship("CatFacultad", back_populates="escuelas")
    personas = relationship("Persona", back_populates="escuela")

class CatCasoSocial(Base):
    __tablename__ = "cat_casos_sociales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    
    personas = relationship("Persona", back_populates="caso_social")

# Modelo Principal: Usuario (Login)
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(200))
    rol = Column(String(20), default="operador") # administrador, operador
    activo = Column(Boolean, default=True)

# Modelo Principal: Persona (Bitácora de Atenciones)
class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(20), index=True, nullable=False) # Permite duplicados para historial
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    edad = Column(Integer)
    sexo = Column(String(1)) # F, M
    fecha_atencion = Column(DateTime, nullable=False, default=datetime.now)
    
    codigo_estudiante = Column(String(20))
    año_estudio = Column(String(10))
    
    tipo_usuario_id = Column(Integer, ForeignKey("cat_tipos_usuario.id"))
    facultad_id = Column(Integer, ForeignKey("cat_facultades.id"))
    escuela_id = Column(Integer, ForeignKey("cat_escuelas.id"))
    caso_social_id = Column(Integer, ForeignKey("cat_casos_sociales.id"))
    
    celular = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(200))
    observaciones = Column(Text)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.now)

    # Relaciones
    tipo_usuario = relationship("CatTipoUsuario", back_populates="personas")
    facultad = relationship("CatFacultad", back_populates="personas")
    escuela = relationship("CatEscuela", back_populates="personas")
    caso_social = relationship("CatCasoSocial", back_populates="personas")
