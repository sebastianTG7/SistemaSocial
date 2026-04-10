from database.db_config import SessionLocal
from sqlalchemy import extract, func, or_
from database.models import Persona, CatTipoUsuario, CatCasoSocial, CatEscuela, CatFacultad

class PersonaController:
    @staticmethod
    def buscar_por_dni(dni):
        """Busca la última atención de una persona por DNI para autocompletar."""
        db = SessionLocal()
        try:
            p = db.query(Persona).filter(Persona.dni == dni).order_by(Persona.id.desc()).first()
            if p:
                return {
                    "nombres": p.nombres, "apellidos": p.apellidos,
                    "edad": p.edad, "sexo": p.sexo,
                    "codigo_estudiante": p.codigo_estudiante,
                    "año_estudio": p.año_estudio,
                    "tipo_usuario_id": p.tipo_usuario_id,
                    "facultad_id": p.facultad_id,
                    "escuela_id": p.escuela_id,
                    "celular": p.celular, "correo": p.correo,
                    "direccion": p.direccion,
                }
            return None
        finally:
            db.close()

    @staticmethod
    def registrar(datos):
        """Registra una nueva atención."""
        from datetime import datetime
        db = SessionLocal()
        try:
            fecha = datetime.strptime(datos["fecha_atencion"], "%d/%m/%Y")
            persona = Persona(
                dni=datos["dni"],
                fecha_atencion=fecha,
                nombres=datos["nombres"].upper(),
                apellidos=datos["apellidos"].upper(),
                edad=int(datos["edad"]) if datos.get("edad") and str(datos["edad"]).isdigit() else None,
                sexo=datos.get("sexo"),
                codigo_estudiante=datos.get("codigo_estudiante"),
                año_estudio=datos.get("año_estudio"),
                tipo_usuario_id=datos.get("tipo_usuario_id"),
                facultad_id=datos.get("facultad_id"),
                escuela_id=datos.get("escuela_id"),
                caso_social_id=datos.get("caso_social_id"),
                celular=datos.get("celular"),
                correo=datos.get("correo"),
                direccion=datos.get("direccion"),
                observaciones=datos.get("observaciones"),
            )
            db.add(persona)
            db.commit()
            return True, persona.id
        except Exception as ex:
            db.rollback()
            return False, str(ex)
        finally:
            db.close()

    @staticmethod
    def get_all(solo_activos=True):
        db = SessionLocal()
        try:
            query = db.query(
                Persona.id, Persona.dni, Persona.nombres, Persona.apellidos,
                Persona.sexo, Persona.edad, Persona.celular, Persona.correo,
                Persona.direccion, Persona.fecha_atencion, Persona.activo,
                Persona.codigo_estudiante, Persona.año_estudio, Persona.observaciones,
                CatTipoUsuario.nombre.label("tipo_usuario"),
                CatCasoSocial.nombre.label("caso_social"),
                CatFacultad.nombre.label("facultad"),
                CatEscuela.nombre.label("escuela")
            ).join(CatTipoUsuario, Persona.tipo_usuario_id == CatTipoUsuario.id)\
             .join(CatCasoSocial, Persona.caso_social_id == CatCasoSocial.id)\
             .join(CatFacultad, Persona.facultad_id == CatFacultad.id)\
             .join(CatEscuela, Persona.escuela_id == CatEscuela.id)
            
            if solo_activos:
                query = query.filter(Persona.activo == True)
            
            results = query.all()
            return [dict(r._asdict()) for r in results]
        finally:
            db.close()

    @staticmethod
    def get_trend(anio):
        db = SessionLocal()
        try:
            trend = db.query(extract('month', Persona.fecha_atencion), func.count(Persona.id))\
                .filter(extract('year', Persona.fecha_atencion) == int(anio))\
                .filter(Persona.activo == True)\
                .group_by(extract('month', Persona.fecha_atencion)).all()
            trend_data = {m: 0 for m in range(1, 13)}
            for m, c in trend: trend_data[int(m)] = c
            return trend_data
        finally:
            db.close()

    @staticmethod
    def get_analytics(mes=None, anio=None):
        db = SessionLocal()
        try:
            # 1. Total
            q_total = db.query(func.count(Persona.id)).filter(Persona.activo == True)
            if mes: q_total = q_total.filter(extract('month', Persona.fecha_atencion) == int(mes))
            if anio: q_total = q_total.filter(extract('year', Persona.fecha_atencion) == int(anio))
            total = q_total.scalar() or 0

            # 2. Tipos
            q_tipos = db.query(CatTipoUsuario.nombre, func.count(Persona.id))\
                .outerjoin(Persona, (Persona.tipo_usuario_id == CatTipoUsuario.id) & (Persona.activo == True))
            if mes: q_tipos = q_tipos.filter(extract('month', Persona.fecha_atencion) == int(mes))
            if anio: q_tipos = q_tipos.filter(extract('year', Persona.fecha_atencion) == int(anio))
            tipos = q_tipos.group_by(CatTipoUsuario.nombre).all()

            # 3. Casos
            q_casos = db.query(CatCasoSocial.nombre, func.count(Persona.id))\
                .outerjoin(Persona, (Persona.caso_social_id == CatCasoSocial.id) & (Persona.activo == True))
            if mes: q_casos = q_casos.filter(extract('month', Persona.fecha_atencion) == int(mes))
            if anio: q_casos = q_casos.filter(extract('year', Persona.fecha_atencion) == int(anio))
            casos = q_casos.group_by(CatCasoSocial.nombre).all()

            # 4. Escuelas (top por escuela, no por facultad)
            q_escu = db.query(CatEscuela.nombre, func.count(Persona.id))\
                .join(Persona, (Persona.escuela_id == CatEscuela.id) & (Persona.activo == True))
            if mes: q_escu = q_escu.filter(extract('month', Persona.fecha_atencion) == int(mes))
            if anio: q_escu = q_escu.filter(extract('year', Persona.fecha_atencion) == int(anio))
            q_escu = q_escu.group_by(CatEscuela.nombre)
            # Top 5 para card principal
            facultades_top5 = q_escu.order_by(func.count(Persona.id).desc()).limit(5).all()
            # Todas para el acordeón
            facultades_todas = q_escu.order_by(func.count(Persona.id).desc()).all()

            # 5. Sexo
            q_sexo = db.query(Persona.sexo, func.count(Persona.id)).filter(Persona.activo == True)
            if mes: q_sexo = q_sexo.filter(extract('month', Persona.fecha_atencion) == int(mes))
            if anio: q_sexo = q_sexo.filter(extract('year', Persona.fecha_atencion) == int(anio))
            sexo = q_sexo.group_by(Persona.sexo).all()

            return {
                "total_periodo": total,
                "tipos": {n: c for n, c in tipos},
                "casos_periodo": {n: c for n, c in casos},
                "top_escuelas": [{"label": n, "count": c} for n, c in facultades_top5],
                "todas_escuelas": [{"label": n, "count": c} for n, c in facultades_todas],
                "sexo": {s if s else "N/A": c for s, c in sexo}
            }
        finally:
            db.close()
            
    @staticmethod
    def desactivar(p_id):
        db = SessionLocal(); p = db.query(Persona).filter(Persona.id == p_id).first()
        if p: p.activo = False; db.commit()
        db.close()

    @staticmethod
    def activar(p_id):
        db = SessionLocal(); p = db.query(Persona).filter(Persona.id == p_id).first()
        if p: p.activo = True; db.commit()
        db.close()

    @staticmethod
    def eliminar_permanente(p_id):
        db = SessionLocal(); p = db.query(Persona).filter(Persona.id == p_id).first()
        if p: db.delete(p); db.commit()
        db.close()
