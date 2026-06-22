import csv
import sys
import os
import unicodedata
from datetime import datetime

# Agregar la ruta raíz a sys.path para poder importar de database/controllers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_config import SessionLocal
from database.models import Persona, FichaSocioeconomica, CatEscuela, CatCasoSocial, CatModalidad

def normalize_string(s):
    if not s:
        return ""
    # Convertir a minúsculas y quitar espacios en los extremos
    s = str(s).strip().lower()
    # Eliminar acentos y tildes
    s = "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    # Reemplazar variantes ortográficas comunes
    s = s.replace("ingeneria", "ingenieria")
    s = s.replace("educacion", "educacion")
    s = s.replace("historico", "historico")
    s = s.replace("politicas", "politicas")
    # Eliminar dobles espacios
    s = " ".join(s.split())
    return s

def to_float(val):
    if not val:
        return 0.0
    try:
        return float(str(val).strip())
    except Exception:
        return 0.0

def to_bool(val):
    if not val:
        return False
    return str(val).strip().upper() in ["VERDADERO", "TRUE", "1", "SÍ", "SI"]

def import_data(dry_run=True):
    txt_path = "nueva_data_discapacidad_junio.txt"
    if not os.path.exists(txt_path):
        print(f"Error: No se encontró el archivo {txt_path}")
        return
        
    db = SessionLocal()
    
    # Pre-cargar catálogos de base de datos
    escuelas = db.query(CatEscuela).all()
    casos = db.query(CatCasoSocial).all()
    modalidades = db.query(CatModalidad).all()
    
    # Crear mappers con nombres normalizados
    escuela_map = {normalize_string(e.nombre): e for e in escuelas}
    caso_map = {normalize_string(c.nombre): c for c in casos}
    modalidad_map = {normalize_string(m.nombre): m for m in modalidades}
    
    print("Mapeando catálogos de la base de datos...")
    print(f"  Escuelas cargadas: {len(escuelas)}")
    print(f"  Casos cargados: {len(casos)}")
    print(f"  Modalidades cargadas: {len(modalidades)}")
    
    rows_to_insert = []
    
    with open(txt_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for idx, raw_row in enumerate(reader, 1):
            # Limpiar llaves del diccionario (quitar espacios en cabecera si los hubiera)
            row = {k.strip(): v for k, v in raw_row.items() if k is not None}
            
            # 1. Validar y mapear Escuela Profesional
            raw_escuela = row.get("escuela_id", "")
            norm_escuela = normalize_string(raw_escuela)
            escuela = escuela_map.get(norm_escuela)
            
            if not escuela:
                print(f"Fila {idx}: Escuela '{raw_escuela}' no encontrada en la base de datos. Abortando.")
                db.close()
                return
                
            # 2. Validar y mapear Caso Social
            raw_caso = row.get("caso_social_id", "")
            norm_caso = normalize_string(raw_caso)
            caso = caso_map.get(norm_caso)
            if not caso:
                if norm_caso == "evaluacion":
                    # Intentar con acento si vino como "Evaluacion"
                    caso = caso_map.get("evaluacion") or caso_map.get("evaluación")
                if not caso:
                    print(f"Fila {idx}: Caso social '{raw_caso}' no encontrado. Abortando.")
                    db.close()
                    return
            
            # 3. Validar y mapear Modalidad de ingreso
            raw_modalidad = row.get("Modalidad de ingreso", "")
            norm_modalidad = normalize_string(raw_modalidad)
            modalidad = modalidad_map.get(norm_modalidad)
            if not modalidad:
                print(f"Fila {idx}: Modalidad '{raw_modalidad}' no encontrada. Abortando.")
                db.close()
                return
                
            # Parsear datos básicos de la persona
            dni = row.get("dni", "").strip()
            nombres = row.get("nombres", "").strip().upper()
            apellidos = row.get("apellidos", "").strip().upper()
            
            edad_str = row.get("edad", "").strip()
            edad = int(edad_str) if edad_str.isdigit() else None
            
            sexo = row.get("sexo", "").strip()
            sexo = sexo if sexo in ["M", "F"] else None
            
            codigo = row.get("codigo_estudiante", "").strip()
            codigo = codigo if codigo else None
            
            anio_estudio = row.get("año_estudio", "").strip()
            anio_estudio = anio_estudio if anio_estudio else None
            
            celular = row.get("celular", "").strip()
            celular = celular if celular else None
            
            correo = row.get("correo", "").strip()
            correo = correo if correo else None
            
            direccion = row.get("direccion", "").strip()
            direccion = direccion if direccion else None
            
            observaciones = row.get("observaciones", "").strip()
            observaciones = observaciones if observaciones else None
            
            codigo_conadis = row.get("CODIGO_CONADIS", "").strip()
            codigo_conadis = codigo_conadis if codigo_conadis else None
            
            nivel_disc = row.get("NIVEL_DE_DISCAPACIDAD", "").strip().title()
            nivel_disc = nivel_disc if nivel_disc in ["Leve", "Moderada", "Severa"] else "Ninguno"
            
            # Ficha Socioeconómica
            sisfoh = row.get("sisfoh_condicion", "").strip()
            sisfoh = sisfoh if sisfoh else None
            
            tiene_disc = to_bool(row.get("tiene_discapacidad"))
            tipo_disc = row.get("tipo_discapacidad", "").strip()
            tipo_disc = tipo_disc if tipo_disc else "Ninguna"
            
            tipo_seguro = row.get("tipo_seguro", "").strip()
            tipo_seguro = tipo_seguro if tipo_seguro else None
            
            est_familiar = row.get("estructura_familiar", "").strip()
            est_familiar = est_familiar if est_familiar else None
            
            din_familiar = row.get("dinamica_familiar", "").strip()
            din_familiar = din_familiar if din_familiar else None
            
            ingreso_fam = to_float(row.get("ingreso_familiar_total"))
            ingreso_beca = to_float(row.get("ingreso_becas_bonos"))
            egreso_alquiler = to_float(row.get("egreso_alquiler"))
            egreso_alimentacion = to_float(row.get("egreso_alimentacion"))
            egreso_servicios = to_float(row.get("egreso_servicios"))
            egreso_educacion = to_float(row.get("egreso_educacion_otros"))
            
            tipo_vivienda = row.get("tipo_vivienda", "").strip()
            tipo_vivienda = tipo_vivienda if tipo_vivienda else None
            
            mat_paredes = row.get("material_paredes", "").strip()
            mat_paredes = mat_paredes if mat_paredes else None
            
            mat_techo = row.get("material_techo", "").strip()
            mat_techo = mat_techo if mat_techo else None
            
            agua = to_bool(row.get("tiene_agua_red"))
            desague = to_bool(row.get("tiene_desague_red"))
            luz = to_bool(row.get("tiene_energia_electrica"))
            
            rows_to_insert.append({
                "persona": Persona(
                    dni=dni,
                    nombres=nombres,
                    apellidos=apellidos,
                    edad=edad,
                    sexo=sexo,
                    codigo_estudiante=codigo,
                    año_estudio=anio_estudio,
                    tipo_usuario_id=1,  # Estudiante
                    facultad_id=escuela.facultad_id,
                    escuela_id=escuela.id,
                    caso_social_id=caso.id,
                    modalidad_id=modalidad.id,
                    registro_modalidad=codigo_conadis,
                    celular=celular,
                    correo=correo,
                    direccion=direccion,
                    observaciones=observaciones,
                    fecha_atencion=datetime.now(),
                    fecha_registro=datetime.now(),
                    activo=True
                ),
                "ficha": FichaSocioeconomica(
                    motivo_evaluacion="Modalidad de ingreso",
                    sisfoh_condicion=sisfoh,
                    tiene_discapacidad=tiene_disc,
                    tipo_discapacidad=tipo_disc,
                    nivel_de_discapacidad=nivel_disc,
                    tipo_seguro=tipo_seguro,
                    estructura_familiar=est_familiar,
                    dinamica_familiar=din_familiar,
                    ingreso_familiar_total=ingreso_fam,
                    ingreso_becas_bonos=ingreso_beca,
                    egreso_alquiler=egreso_alquiler,
                    egreso_alimentacion=egreso_alimentacion,
                    egreso_servicios=egreso_servicios,
                    egreso_educacion_otros=egreso_educacion,
                    tipo_vivienda=tipo_vivienda,
                    material_paredes=mat_paredes,
                    material_techo=mat_techo,
                    tiene_agua_red=agua,
                    tiene_desague_red=desague,
                    tiene_energia_electrica=luz
                )
            })
            
    print(f"\nSe procesaron exitosamente {len(rows_to_insert)} registros del archivo.")
    
    if dry_run:
        print("\n--- MODO PRUEBA (DRY RUN) ---")
        print("Registros listos para insertar (primeros 5):")
        escuela_by_id = {e.id: e.nombre for e in escuelas}
        for i, item in enumerate(rows_to_insert[:5], 1):
            p = item["persona"]
            f = item["ficha"]
            print(f"[{i}] {p.apellidos}, {p.nombres} - DNI: {p.dni}")
            print(f"    Escuela: ID {p.escuela_id} ({escuela_by_id.get(p.escuela_id, 'Desconocida')}), Caso ID: {p.caso_social_id}, Modalidad ID: {p.modalidad_id}")
            print(f"    Registro Modalidad (CONADIS): {p.registro_modalidad}")
            print(f"    Ficha -> Sisfoh: {f.sisfoh_condicion}, Discapacidad: {f.tiene_discapacidad} ({f.tipo_discapacidad}, Nivel: {f.nivel_de_discapacidad})")
            print(f"    Económico -> Ingreso: {f.ingreso_familiar_total}, Egreso Alquiler: {f.egreso_alquiler}")
            print(f"    Servicios -> Agua: {f.tiene_agua_red}, Desagüe: {f.tiene_desague_red}, Luz: {f.tiene_energia_electrica}")
        print("\n[OK] Validación exitosa. Para insertar realmente en la base de datos, ejecuta:")
        print("  fletenv\\Scripts\\python scripts\\import_discapacidad_junio.py --run")
    else:
        print("\nInsertando registros reales en la base de datos...")
        try:
            for item in rows_to_insert:
                p = item["persona"]
                f = item["ficha"]
                db.add(p)
                db.flush() # Generar ID para p
                f.persona_id = p.id
                db.add(f)
            db.commit()
            print(f"  [OK] ¡Inserción exitosa! Se insertaron {len(rows_to_insert)} estudiantes y sus fichas socioeconómicas correspondientes.")
        except Exception as ex:
            db.rollback()
            print(f"Error al insertar en la base de datos: {str(ex)}")
            
    db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Importar datos de discapacidad de junio.")
    parser.add_argument("--run", action="store_true", help="Ejecutar la inserción real en la base de datos.")
    args = parser.parse_args()
    
    import_data(dry_run=not args.run)
