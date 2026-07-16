from database.db_config import SessionLocal
from sqlalchemy import extract, func, or_
from database.models import Persona, Atencion, CatTipoUsuario, CatCasoSocial, CatEscuela, CatFacultad, CatModalidad, FichaSocioeconomica

class PersonaController:
    @staticmethod
    def buscar_por_dni(dni):
        """Busca la persona y su última atención por DNI para autocompletar."""
        db = SessionLocal()
        try:
            p = db.query(Persona).filter(Persona.dni == dni).first()
            if p:
                # Buscar la ultima atencion
                a = db.query(Atencion).filter(Atencion.persona_id == p.id).order_by(Atencion.id.desc()).first()
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
                    "fecha_atencion": a.fecha_atencion if a else None,
                    "modalidad_id": a.modalidad_id if a else None,
                    "registro_modalidad": a.registro_modalidad if a else None,
                }
            return None
        finally:
            db.close()

    @staticmethod
    def registrar(datos):
        """Registra una nueva atención. Crea o actualiza la persona si es necesario."""
        from datetime import datetime
        db = SessionLocal()
        try:
            fecha = datetime.strptime(datos["fecha_atencion"], "%d/%m/%Y")
            
            p = db.query(Persona).filter(Persona.dni == datos["dni"]).first()
            if not p:
                p = Persona(dni=datos["dni"])
                db.add(p)
                db.flush() # Para obtener el ID

            # Actualizamos datos estáticos
            p.nombres = datos["nombres"].upper()
            p.apellidos = datos["apellidos"].upper()
            p.edad = int(datos["edad"]) if datos.get("edad") and str(datos["edad"]).isdigit() else p.edad
            p.sexo = datos.get("sexo") or p.sexo
            p.codigo_estudiante = datos.get("codigo_estudiante") or p.codigo_estudiante
            p.año_estudio = datos.get("año_estudio") or p.año_estudio
            p.tipo_usuario_id = datos.get("tipo_usuario_id") or p.tipo_usuario_id
            p.facultad_id = datos.get("facultad_id") or p.facultad_id
            p.escuela_id = datos.get("escuela_id") or p.escuela_id
            p.celular = datos.get("celular") or p.celular
            p.correo = datos.get("correo") or p.correo
            p.direccion = datos.get("direccion") or p.direccion
            
            db.flush()

            # Creamos la atención
            a = Atencion(
                persona_id=p.id,
                fecha_atencion=fecha,
                caso_social_id=datos.get("caso_social_id"),
                modalidad_id=datos.get("modalidad_id"),
                registro_modalidad=datos.get("registro_modalidad"),
                observaciones=datos.get("observaciones"),
            )
            db.add(a)
            db.commit()
            return True, a.id  # Devolvemos el ID de la atencion!
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
                Atencion.id, Persona.dni, Persona.nombres, Persona.apellidos,
                Persona.sexo, Persona.edad, Persona.celular, Persona.correo,
                Persona.direccion, Atencion.fecha_atencion, Atencion.activo,
                Persona.codigo_estudiante, Persona.año_estudio, Atencion.observaciones,
                Atencion.modalidad_id, Atencion.registro_modalidad,
                CatTipoUsuario.nombre.label("tipo_usuario"),
                CatCasoSocial.nombre.label("caso_social"),
                CatFacultad.nombre.label("facultad"),
                CatEscuela.nombre.label("escuela"),
                CatModalidad.nombre.label("modalidad"),
                FichaSocioeconomica.id.isnot(None).label("tiene_ficha")
            ).select_from(Atencion).join(Persona, Atencion.persona_id == Persona.id)\
             .outerjoin(CatTipoUsuario, Persona.tipo_usuario_id == CatTipoUsuario.id)\
             .outerjoin(CatCasoSocial, Atencion.caso_social_id == CatCasoSocial.id)\
             .outerjoin(CatFacultad, Persona.facultad_id == CatFacultad.id)\
             .outerjoin(CatEscuela, Persona.escuela_id == CatEscuela.id)\
             .outerjoin(CatModalidad, Atencion.modalidad_id == CatModalidad.id)\
             .outerjoin(FichaSocioeconomica, Persona.id == FichaSocioeconomica.persona_id)
            
            if solo_activos:
                query = query.filter(Atencion.activo == True)
            
            results = query.all()
            return [dict(r._asdict()) for r in results]
        finally:
            db.close()

    @staticmethod
    def get_trend(anio):
        db = SessionLocal()
        try:
            trend = db.query(extract('month', Atencion.fecha_atencion), func.count(Atencion.id))\
                .filter(extract('year', Atencion.fecha_atencion) == int(anio))\
                .filter(Atencion.activo == True)\
                .group_by(extract('month', Atencion.fecha_atencion)).all()
            trend_data = {m: 0 for m in range(1, 13)}
            for m, c in trend: trend_data[int(m)] = c
            return trend_data
        finally:
            db.close()

    @staticmethod
    def get_analytics(mes=None, anio=None):
        db = SessionLocal()
        try:
            # 1. Total (Atenciones)
            q_total = db.query(func.count(Atencion.id)).filter(Atencion.activo == True)
            if mes: q_total = q_total.filter(extract('month', Atencion.fecha_atencion) == int(mes))
            if anio: q_total = q_total.filter(extract('year', Atencion.fecha_atencion) == int(anio))
            total = q_total.scalar() or 0

            # 2. Tipos
            q_tipos = db.query(CatTipoUsuario.nombre, func.count(Atencion.id))\
                .select_from(Atencion).join(Persona, Atencion.persona_id == Persona.id)\
                .outerjoin(CatTipoUsuario, Persona.tipo_usuario_id == CatTipoUsuario.id)\
                .filter(Atencion.activo == True)
            if mes: q_tipos = q_tipos.filter(extract('month', Atencion.fecha_atencion) == int(mes))
            if anio: q_tipos = q_tipos.filter(extract('year', Atencion.fecha_atencion) == int(anio))
            tipos = q_tipos.group_by(CatTipoUsuario.nombre).all()

            # 3. Casos
            q_casos = db.query(CatCasoSocial.nombre, func.count(Atencion.id))\
                .select_from(Atencion)\
                .outerjoin(CatCasoSocial, Atencion.caso_social_id == CatCasoSocial.id)\
                .filter(Atencion.activo == True)
            if mes: q_casos = q_casos.filter(extract('month', Atencion.fecha_atencion) == int(mes))
            if anio: q_casos = q_casos.filter(extract('year', Atencion.fecha_atencion) == int(anio))
            casos = q_casos.group_by(CatCasoSocial.nombre).all()

            # 4. Escuelas
            q_escu = db.query(CatEscuela.nombre, func.count(Atencion.id))\
                .select_from(Atencion).join(Persona, Atencion.persona_id == Persona.id)\
                .join(CatEscuela, Persona.escuela_id == CatEscuela.id)\
                .filter(Atencion.activo == True)
            if mes: q_escu = q_escu.filter(extract('month', Atencion.fecha_atencion) == int(mes))
            if anio: q_escu = q_escu.filter(extract('year', Atencion.fecha_atencion) == int(anio))
            q_escu = q_escu.group_by(CatEscuela.nombre)
            facultades_top5 = q_escu.order_by(func.count(Atencion.id).desc()).limit(5).all()
            facultades_todas = q_escu.order_by(func.count(Atencion.id).desc()).all()

            # 5. Sexo
            q_sexo = db.query(Persona.sexo, func.count(Atencion.id))\
                .select_from(Atencion).join(Persona, Atencion.persona_id == Persona.id)\
                .filter(Atencion.activo == True)
            if mes: q_sexo = q_sexo.filter(extract('month', Atencion.fecha_atencion) == int(mes))
            if anio: q_sexo = q_sexo.filter(extract('year', Atencion.fecha_atencion) == int(anio))
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
    def desactivar(a_id):
        db = SessionLocal(); a = db.query(Atencion).filter(Atencion.id == a_id).first()
        if a: a.activo = False; db.commit()
        db.close()

    @staticmethod
    def activar(a_id):
        db = SessionLocal(); a = db.query(Atencion).filter(Atencion.id == a_id).first()
        if a: a.activo = True; db.commit()
        db.close()

    @staticmethod
    def eliminar_permanente(a_id):
        db = SessionLocal(); a = db.query(Atencion).filter(Atencion.id == a_id).first()
        if a: db.delete(a); db.commit()
        db.close()

    @staticmethod
    def get_ficha_socioeconomica(atencion_id):
        from database.db_config import SessionLocal
        from database.models import FichaSocioeconomica, Atencion
        db = SessionLocal()
        try:
            # La ficha está ligada a Persona, así que buscamos la persona vía Atencion
            atencion = db.query(Atencion).filter(Atencion.id == atencion_id).first()
            if not atencion: return None
            
            ficha = db.query(FichaSocioeconomica).filter(FichaSocioeconomica.persona_id == atencion.persona_id).first()
            if ficha:
                return {
                    "id": ficha.id,
                    "persona_id": ficha.persona_id,
                    "motivo_evaluacion": ficha.motivo_evaluacion,
                    "sisfoh_condicion": ficha.sisfoh_condicion,
                    "tiene_discapacidad": ficha.tiene_discapacidad,
                    "tipo_discapacidad": ficha.tipo_discapacidad,
                    "nivel_de_discapacidad": ficha.nivel_de_discapacidad,
                    "tipo_seguro": ficha.tipo_seguro,
                    "estructura_familiar": ficha.estructura_familiar,
                    "dinamica_familiar": ficha.dinamica_familiar,
                    "ingreso_familiar_total": ficha.ingreso_familiar_total,
                    "ingreso_becas_bonos": ficha.ingreso_becas_bonos,
                    "egreso_alquiler": ficha.egreso_alquiler,
                    "egreso_alimentacion": ficha.egreso_alimentacion,
                    "egreso_servicios": ficha.egreso_servicios,
                    "egreso_educacion_otros": ficha.egreso_educacion_otros,
                    "tipo_vivienda": ficha.tipo_vivienda,
                    "material_paredes": ficha.material_paredes,
                    "material_techo": ficha.material_techo,
                    "tiene_agua_red": ficha.tiene_agua_red,
                    "tiene_desague_red": ficha.tiene_desague_red,
                    "tiene_energia_electrica": ficha.tiene_energia_electrica
                }
            return None
        finally:
            db.close()

    @staticmethod
    def guardar_ficha_socioeconomica(atencion_id, datos):
        from database.db_config import SessionLocal
        from database.models import FichaSocioeconomica, Atencion
        db = SessionLocal()
        try:
            atencion = db.query(Atencion).filter(Atencion.id == atencion_id).first()
            if not atencion: return False, "Atención no encontrada"
            
            ficha = db.query(FichaSocioeconomica).filter(FichaSocioeconomica.persona_id == atencion.persona_id).first()
            if not ficha:
                ficha = FichaSocioeconomica(persona_id=atencion.persona_id)
                db.add(ficha)
            
            ficha.motivo_evaluacion = datos.get("motivo_evaluacion")
            ficha.sisfoh_condicion = datos.get("sisfoh_condicion")
            ficha.tiene_discapacidad = bool(datos.get("tiene_discapacidad"))
            ficha.tipo_discapacidad = datos.get("tipo_discapacidad") if bool(datos.get("tiene_discapacidad")) else "Ninguna"
            ficha.nivel_de_discapacidad = datos.get("nivel_de_discapacidad") if bool(datos.get("tiene_discapacidad")) else "Ninguno"
            ficha.tipo_seguro = datos.get("tipo_seguro")
            ficha.estructura_familiar = datos.get("estructura_familiar")
            ficha.dinamica_familiar = datos.get("dinamica_familiar")
            
            # Convert values to float safely
            def to_float(val):
                try: return float(val) if val else 0.0
                except: return 0.0
                
            ficha.ingreso_familiar_total = to_float(datos.get("ingreso_familiar_total"))
            ficha.ingreso_becas_bonos = to_float(datos.get("ingreso_becas_bonos"))
            ficha.egreso_alquiler = to_float(datos.get("egreso_alquiler"))
            ficha.egreso_alimentacion = to_float(datos.get("egreso_alimentacion"))
            ficha.egreso_servicios = to_float(datos.get("egreso_servicios"))
            ficha.egreso_educacion_otros = to_float(datos.get("egreso_educacion_otros"))
            
            ficha.tipo_vivienda = datos.get("tipo_vivienda")
            ficha.material_paredes = datos.get("material_paredes")
            ficha.material_techo = datos.get("material_techo")
            ficha.tiene_agua_red = bool(datos.get("tiene_agua_red"))
            ficha.tiene_desague_red = bool(datos.get("tiene_desague_red"))
            ficha.tiene_energia_electrica = bool(datos.get("tiene_energia_electrica"))
            
            db.commit()
            return True, ficha.id
        except Exception as ex:
            db.rollback()
            return False, str(ex)
        finally:
            db.close()

    @staticmethod
    def get_socioeconomic_analytics():
        from database.db_config import SessionLocal
        from database.models import FichaSocioeconomica, Persona
        db = SessionLocal()
        try:
            # Query all active evaluations
            fichas = db.query(FichaSocioeconomica).join(Persona, Persona.id == FichaSocioeconomica.persona_id).filter(Persona.activo == True).all()
            
            total = len(fichas)
            
            # 1. SISFOH Condicion
            sisfoh = {"No Pobre": 0, "Pobre": 0, "Pobre Extremo": 0}
            for f in fichas:
                cond = f.sisfoh_condicion
                if cond in sisfoh:
                    sisfoh[cond] += 1
                    
            # 2. Servicios Básicos
            agua = sum(1 for f in fichas if f.tiene_agua_red)
            desague = sum(1 for f in fichas if f.tiene_desague_red)
            luz = sum(1 for f in fichas if f.tiene_energia_electrica)
            
            # 3. Datos Económicos Promedio
            avg_ingreso = sum(f.ingreso_familiar_total for f in fichas) / total if total > 0 else 0.0
            avg_becas = sum(f.ingreso_becas_bonos for f in fichas) / total if total > 0 else 0.0
            
            avg_alquiler = sum(f.egreso_alquiler for f in fichas) / total if total > 0 else 0.0
            avg_alimentacion = sum(f.egreso_alimentacion for f in fichas) / total if total > 0 else 0.0
            avg_servicios = sum(f.egreso_servicios for f in fichas) / total if total > 0 else 0.0
            avg_educacion = sum(f.egreso_educacion_otros for f in fichas) / total if total > 0 else 0.0
            
            # 4. Motivos de Evaluación
            motivos = {}
            for f in fichas:
                mot = f.motivo_evaluacion or "No especificado"
                motivos[mot] = motivos.get(mot, 0) + 1
                
            return {
                "total": total,
                "sisfoh": sisfoh,
                "agua_red": agua,
                "desague_red": desague,
                "energia_electrica": luz,
                "avg_ingreso_familiar": avg_ingreso,
                "avg_becas_bonos": avg_becas,
                "avg_egreso_alquiler": avg_alquiler,
                "avg_egreso_alimentacion": avg_alimentacion,
                "avg_egreso_servicios": avg_servicios,
                "avg_egreso_educacion": avg_educacion,
                "motivos": motivos
            }
        finally:
            db.close()

    @staticmethod
    def get_ficha_derivacion(atencion_id):
        from database.db_config import SessionLocal
        from database.models import FichaDerivacion
        db = SessionLocal()
        try:
            ficha = db.query(FichaDerivacion).filter(FichaDerivacion.atencion_id == atencion_id).first()
            if ficha:
                return {
                    "id": ficha.id,
                    "atencion_id": ficha.atencion_id,
                    "lugar_nacimiento": ficha.lugar_nacimiento,
                    "ocupacion": ficha.ocupacion,
                    "vive_con": ficha.vive_con,
                    "telefono_familiares": ficha.telefono_familiares,
                    "area_deriva": ficha.area_deriva,
                    "area_derivada": ficha.area_derivada,
                    "fecha_derivacion": ficha.fecha_derivacion,
                    "motivo_consulta": ficha.motivo_consulta,
                    "tiene_derivaciones_previas": ficha.tiene_derivaciones_previas,
                    "detalle_derivaciones_previas": ficha.detalle_derivaciones_previas,
                    "condicion": ficha.condicion,
                    "impacto_academico": ficha.impacto_academico,
                    "impacto_social": ficha.impacto_social,
                    "impacto_familiar": ficha.impacto_familiar,
                    "impacto_personal": ficha.impacto_personal,
                    "diagnostico": ficha.diagnostico,
                    "observaciones": ficha.observaciones
                }
            return None
        finally:
            db.close()

    @staticmethod
    def guardar_ficha_derivacion(atencion_id, datos):
        from database.db_config import SessionLocal
        from database.models import FichaDerivacion
        from datetime import datetime
        db = SessionLocal()
        try:
            ficha = db.query(FichaDerivacion).filter(FichaDerivacion.atencion_id == atencion_id).first()
            if not ficha:
                ficha = FichaDerivacion(atencion_id=atencion_id)
                db.add(ficha)
            
            if datos.get("fecha_derivacion"):
                try:
                    ficha.fecha_derivacion = datetime.strptime(datos["fecha_derivacion"], "%d/%m/%Y")
                except:
                    pass
                    
            ficha.lugar_nacimiento = datos.get("lugar_nacimiento")
            ficha.ocupacion = datos.get("ocupacion")
            ficha.vive_con = datos.get("vive_con")
            ficha.telefono_familiares = datos.get("telefono_familiares")
            
            ficha.area_deriva = datos.get("area_deriva")
            ficha.area_derivada = datos.get("area_derivada")
            
            ficha.motivo_consulta = datos.get("motivo_consulta")
            ficha.tiene_derivaciones_previas = bool(datos.get("tiene_derivaciones_previas"))
            ficha.detalle_derivaciones_previas = datos.get("detalle_derivaciones_previas")
            ficha.condicion = datos.get("condicion")
            
            ficha.impacto_academico = bool(datos.get("impacto_academico"))
            ficha.impacto_social = bool(datos.get("impacto_social"))
            ficha.impacto_familiar = bool(datos.get("impacto_familiar"))
            ficha.impacto_personal = bool(datos.get("impacto_personal"))
            
            ficha.diagnostico = datos.get("diagnostico")
            ficha.observaciones = datos.get("observaciones")
            
            db.commit()
            return True, ficha.id
        except Exception as ex:
            db.rollback()
            return False, str(ex)
        finally:
            db.close()
