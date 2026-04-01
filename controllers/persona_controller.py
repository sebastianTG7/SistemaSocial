from database.db_config import SessionLocal
from database.models import Persona
from datetime import datetime


class PersonaController:

    @staticmethod
    def registrar(datos: dict):
        """Registra una nueva atención para una persona. Permite múltiples registros por DNI."""
        db = SessionLocal()
        try:
            # Procesar fecha manual o usar hoy
            f_str = datos.get("fecha_atencion")
            if f_str:
                try:
                    fecha_val = datetime.strptime(f_str, "%d/%m/%Y")
                except:
                    fecha_val = datetime.now()
            else:
                fecha_val = datetime.now()

            persona = Persona(
                dni=datos["dni"],
                nombres=datos["nombres"].strip().upper(),
                apellidos=datos["apellidos"].strip().upper(),
                edad=int(datos["edad"]) if datos.get("edad") else None,
                sexo=datos.get("sexo"),
                fecha_atencion=fecha_val,
                codigo_estudiante=datos.get("codigo_estudiante", "").strip() or None,
                año_estudio=datos.get("año_estudio", "").strip() or None,
                tipo_usuario_id=datos.get("tipo_usuario_id"),
                facultad_id=datos.get("facultad_id"),
                escuela_id=datos.get("escuela_id"),
                caso_social_id=datos.get("caso_social_id"),
                celular=datos.get("celular", "").strip() or None,
                correo=datos.get("correo", "").strip() or None,
                direccion=datos.get("direccion", "").strip() or None,
                observaciones=datos.get("observaciones", "").strip() or None,
            )
            db.add(persona)
            db.commit()
            db.refresh(persona)
            return True, persona
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def buscar_por_dni(dni: str):
        """Busca el último registro de una persona por DNI para autocompletar."""
        db = SessionLocal()
        try:
            p = db.query(Persona).filter(Persona.dni == dni).order_by(Persona.id.desc()).first()
            if p:
                return {
                    "nombres": p.nombres,
                    "apellidos": p.apellidos,
                    "edad": p.edad,
                    "sexo": p.sexo,
                    "codigo_estudiante": p.codigo_estudiante,
                    "año_estudio": p.año_estudio,
                    "tipo_usuario_id": p.tipo_usuario_id,
                    "facultad_id": p.facultad_id,
                    "escuela_id": p.escuela_id,
                    "celular": p.celular,
                    "correo": p.correo,
                    "direccion": p.direccion
                }
            return None
        finally:
            db.close()

    @staticmethod
    def get_all(solo_activos=True):
        """Retorna todas las personas con su fecha de atención."""
        db = SessionLocal()
        try:
            query = db.query(Persona)
            if solo_activos:
                query = query.filter(Persona.activo == True)
            personas = query.order_by(Persona.fecha_atencion.desc()).all()
            result = []
            for p in personas:
                result.append({
                    "id": p.id,
                    "dni": p.dni,
                    "nombres": p.nombres,
                    "apellidos": p.apellidos,
                    "edad": p.edad,
                    "sexo": p.sexo,
                    "fecha_atencion": p.fecha_atencion,
                    "codigo_estudiante": p.codigo_estudiante,
                    "año_estudio": p.año_estudio,
                    "tipo_usuario": p.tipo_usuario.nombre if p.tipo_usuario else "-",
                    "tipo_usuario_id": p.tipo_usuario_id,
                    "facultad": p.facultad.nombre if p.facultad else "-",
                    "facultad_id": p.facultad_id,
                    "escuela": p.escuela.nombre if p.escuela else "-",
                    "escuela_id": p.escuela_id,
                    "caso_social": p.caso_social.nombre if p.caso_social else "-",
                    "caso_social_id": p.caso_social_id,
                    "celular": p.celular,
                    "correo": p.correo,
                    "direccion": p.direccion,
                    "observaciones": p.observaciones,
                    "activo": p.activo,
                })
            return result
        finally:
            db.close()

    @staticmethod
    def desactivar(persona_id: int):
        db = SessionLocal()
        try:
            persona = db.query(Persona).filter(Persona.id == persona_id).first()
            if persona:
                persona.activo = False
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def activar(persona_id: int):
        """Reactiva un registro marcado como inactivo."""
        db = SessionLocal()
        try:
            persona = db.query(Persona).filter(Persona.id == persona_id).first()
            if persona:
                persona.activo = True
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def eliminar_permanente(persona_id: int):
        """Borrado físico real de la base de datos."""
        db = SessionLocal()
        try:
            persona = db.query(Persona).filter(Persona.id == persona_id).first()
            if persona:
                db.delete(persona)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def contar_activos():
        db = SessionLocal()
        try:
            return db.query(Persona).filter(Persona.activo == True).count()
        finally:
            db.close()

    @staticmethod
    def contar_por_caso_social():
        from database.models import CatCasoSocial
        from sqlalchemy import func
        db = SessionLocal()
        try:
            stats = db.query(CatCasoSocial.nombre, func.count(Persona.id))\
                .outerjoin(Persona, (Persona.caso_social_id == CatCasoSocial.id) & (Persona.activo == True))\
                .group_by(CatCasoSocial.nombre).all()
            return {nombre: conteo for nombre, conteo in stats}
        finally:
            db.close()
