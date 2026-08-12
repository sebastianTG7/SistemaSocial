from database.db_config import SessionLocal
from database.models import Persona, CatTipoUsuario, CatFacultad, CatEscuela, CatCasoSocial, CatModalidad


class CatalogController:
    @staticmethod
    def get_modalidades():
        db = SessionLocal()
        try:
            return db.query(CatModalidad).filter(CatModalidad.activo == True).order_by(CatModalidad.nombre).all()
        finally:
            db.close()

    @staticmethod
    def get_tipos_usuario():
        db = SessionLocal()
        try:
            return db.query(CatTipoUsuario).filter(CatTipoUsuario.activo == True).all()
        finally:
            db.close()

    @staticmethod
    def get_casos_sociales():
        db = SessionLocal()
        try:
            return db.query(CatCasoSocial).filter(CatCasoSocial.activo == True).all()
        finally:
            db.close()

    @staticmethod
    def get_or_create_caso_social(nombre_caso: str) -> int:
        if not nombre_caso:
            return None
        db = SessionLocal()
        try:
            caso = db.query(CatCasoSocial).filter(CatCasoSocial.nombre == nombre_caso).first()
            if not caso:
                caso = CatCasoSocial(nombre=nombre_caso, activo=True)
                db.add(caso)
                db.commit()
                db.refresh(caso)
            return caso.id
        finally:
            db.close()

    @staticmethod
    def get_facultades():
        db = SessionLocal()
        try:
            return db.query(CatFacultad).filter(CatFacultad.activo == True).order_by(CatFacultad.nombre).all()
        finally:
            db.close()

    @staticmethod
    def get_escuelas_by_facultad(facultad_id: int):
        db = SessionLocal()
        try:
            return (
                db.query(CatEscuela)
                .filter(CatEscuela.facultad_id == facultad_id, CatEscuela.activo == True)
                .order_by(CatEscuela.nombre)
                .all()
            )
        finally:
            db.close()
