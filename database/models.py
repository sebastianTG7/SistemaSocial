from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Enum, Text, Float
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

# Tipo de Casos Sociales: Orientacion, Evaluacion, Seguimiento-Evaluacion y Seguimiento.
class CatCasoSocial(Base):
    __tablename__ = "cat_casos_sociales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    
    personas = relationship("Persona", back_populates="caso_social")

# Tipo de Modalidades de ingreso: General, Cepreval, Discapacidad, Hijos de campesino, Violencia Politica ...
class CatModalidad(Base):
    __tablename__ = "cat_modalidades"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    
    personas = relationship("Persona", back_populates="modalidad")

# Modelo Principal: Usuario (Login)
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(200))
    rol = Column(String(20), default="operador") # administrador, operador
    activo = Column(Boolean, default=True)

# Modelo Principal: Persona o Estudiantes (Bitácora de Atenciones)
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
    modalidad_id = Column(Integer, ForeignKey("cat_modalidades.id"))
    registro_modalidad = Column(String(100))
    
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
    modalidad = relationship("CatModalidad", back_populates="personas")
    ficha_socioeconomica = relationship("FichaSocioeconomica", uselist=False, back_populates="persona", cascade="all, delete-orphan")
    ficha_derivacion = relationship("FichaDerivacion", uselist=False, back_populates="persona", cascade="all, delete-orphan")


class FichaSocioeconomica(Base):
    __tablename__ = "fichas_socioeconomicas"
    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False, unique=True)
    
    # Contexto de la Evaluación
    motivo_evaluacion = Column(String(100))
    
    # Clasificación de Vulnerabilidad (SISFOH y Salud)
    sisfoh_condicion = Column(String(50))
    tiene_discapacidad = Column(Boolean, default=False)
    tipo_discapacidad = Column(String(50))
    nivel_de_discapacidad = Column(String(50))
    tipo_seguro = Column(String(50))
    
    # Estructura y Dinámica Familiar
    estructura_familiar = Column(String(50))
    dinamica_familiar = Column(String(50))
    
    # Datos Económicos
    ingreso_familiar_total = Column(Float, default=0.0)
    ingreso_becas_bonos = Column(Float, default=0.0)
    egreso_alquiler = Column(Float, default=0.0)
    egreso_alimentacion = Column(Float, default=0.0)
    egreso_servicios = Column(Float, default=0.0)
    egreso_educacion_otros = Column(Float, default=0.0)
    
    # Características de la Vivienda
    tipo_vivienda = Column(String(50))
    material_paredes = Column(String(50))
    material_techo = Column(String(50))
    tiene_agua_red = Column(Boolean, default=False)
    tiene_desague_red = Column(Boolean, default=False)
    tiene_energia_electrica = Column(Boolean, default=False)
    
    # Relaciones
    persona = relationship("Persona", back_populates="ficha_socioeconomica")

class FichaDerivacion(Base):
    __tablename__ = "fichas_derivacion"
    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False, unique=True)
    
    # Datos Personales Complementarios
    fecha_nacimiento = Column(Date)
    lugar_nacimiento = Column(String(100))
    ocupacion = Column(String(100))
    vive_con = Column(String(100))
    telefono_familiares = Column(String(50))
    
    # Información de los Organismos
    area_deriva = Column(String(100))
    area_derivada = Column(String(100))
    
    # Información de la Derivación
    fecha_derivacion = Column(DateTime, default=datetime.now)
    motivo_consulta = Column(Text)
    tiene_derivaciones_previas = Column(Boolean, default=False)
    detalle_derivaciones_previas = Column(Text)
    condicion = Column(String(50)) # Leve, Moderado, Grave
    
    # Impacto en el funcionamiento diario
    impacto_academico = Column(Boolean, default=False)
    impacto_social = Column(Boolean, default=False)
    impacto_familiar = Column(Boolean, default=False)
    impacto_personal = Column(Boolean, default=False)
    
    diagnostico = Column(Text)
    observaciones = Column(Text)
    
    # Relaciones
    persona = relationship("Persona", back_populates="ficha_derivacion")

