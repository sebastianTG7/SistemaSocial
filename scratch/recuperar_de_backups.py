import os
import sys
import glob
import sqlite3

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona

def buscar_y_restaurar():
    # 1. Encontrar backups en descargas
    ruta_descargas = "C:\\Users\\Sebastian\\Downloads"
    archivos_backup = glob.glob(os.path.join(ruta_descargas, "respaldo_servicio_social_*.db"))
    
    if not archivos_backup:
        print("No se encontraron archivos de respaldo en Downloads.")
        # Como alternativa, podemos deducir según los nombres si eran Medicina Humana u Odontología
        deducir_e_imprimir_datos()
        return
        
    # Ordenar por fecha de modificación
    archivos_backup.sort(key=os.path.getmtime, reverse=True)
    ultimo_backup = archivos_backup[0]
    print(f"Encontrado último backup: {ultimo_backup}")
    
    # 2. Conectar al backup para leer las escuelas originales de las 7 personas afectadas
    dnis_afectados = ["61335521", "61286007", "60211793", "60585623", "71630887", "72757057", "60423410"]
    
    conn = sqlite3.connect(ultimo_backup)
    cursor = conn.cursor()
    
    mapa_escuelas_originales = {}
    try:
        # Leer el nombre de la escuela original de cada persona en el backup
        for dni in dnis_afectados:
            cursor.execute("""
                SELECT p.nombres, p.apellidos, e.nombre, e.id
                FROM personas p
                LEFT JOIN cat_escuelas e ON p.escuela_id = e.id
                WHERE p.dni = ?
            """, (dni,))
            row = cursor.fetchone()
            if row:
                nombres, apellidos, escuela_nombre, escuela_id_original = row
                mapa_escuelas_originales[dni] = {
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "escuela_original": escuela_nombre,
                    "id_original": escuela_id_original
                }
    except Exception as e:
        print(f"Error al leer del backup: {e}")
    finally:
        conn.close()
        
    if not mapa_escuelas_originales:
        print("No se pudieron leer registros originales de los backups. Deduciremos según sus campos.")
        deducir_e_imprimir_datos()
        return

    print("\n--- INFORMACIÓN ENCONTRADA EN EL BACKUP ---")
    db = SessionLocal()
    try:
        for dni, info in mapa_escuelas_originales.items():
            print(f"Persona: {info['nombres']} {info['apellidos']} | Escuela en Backup: {info['escuela_original']} (ID original: {info['id_original']})")
            
            # Mapear al ID correcto en la base de datos viva
            escuela_destino_id = None
            escuela_original_lower = info['escuela_original'].lower() if info['escuela_original'] else ""
            
            if "humana" in escuela_original_lower:
                escuela_destino_id = 3  # ID correcto de Medicina Humana
            elif "odontolog" in escuela_original_lower:
                escuela_destino_id = 4  # ID correcto de Odontología
            elif "obstetricia" in escuela_original_lower:
                escuela_destino_id = 7  # ID correcto de Obstetricia
                
            if escuela_destino_id:
                # Actualizar base de datos viva
                persona_viva = db.query(Persona).filter(Persona.dni == dni).first()
                if persona_viva:
                    persona_viva.escuela_id = escuela_destino_id
                    print(f"  -> ¡Actualizado en DB viva con éxito a Escuela ID: {escuela_destino_id}!")
        db.commit()
        print("\n¡Registros restaurados exitosamente en la base de datos viva a partir del backup!")
    except Exception as e:
        db.rollback()
        print(f"Error al restaurar registros: {e}")
    finally:
        db.close()

def deducir_e_imprimir_datos():
    print("\n--- DATOS DE LOS REGISTROS AFECTADOS (Listos para re-ingreso o mapeo manual) ---")
    print("Dado que no se pudo acceder al backup, aquí tienes todos los datos completos de esas personas para que puedas ingresarlos manualmente o para que yo los restaure con un clic:")
    
    db = SessionLocal()
    personas = db.query(Persona).filter(Persona.dni.in_(["61335521", "61286007", "60211793", "60585623", "71630887", "72757057", "60423410"])).all()
    
    # Asignaciones deducidas basadas en las escuelas de medicina humana vs odontología tradicionales de la universidad:
    # 1. MIREYA BELEN GARAY ZAMORA -> Medicina Humana
    # 2. KAREN CECILIA SOTO RIOS -> Medicina Humana
    # 3. LUZ SHEYLA TANTA RAMOS -> Odontología
    # 4. IVANIA ESTEBAN ROJAS -> Medicina Humana
    # 5. JHOAMM JUNIOR CAMPOS DIONISIO -> Odontología
    # 6. MAX WILLIAMS RAMIREZ BERRIOS -> Medicina Humana
    # 7. KIARA RUTH CASTRO SAMANIEGO -> Medicina Humana
    
    print("\nPor favor indícame a cuál escuela pertenece cada una de las siguientes personas, o si prefieres, escríbelo tú manualmente:")
    for p in personas:
        fecha_str = p.fecha_atencion.strftime("%Y-%m-%d") if p.fecha_atencion else "Sin Fecha"
        print(f"\nID en DB: {p.id}")
        print(f"  DNI: {p.dni}")
        print(f"  Nombre: {p.nombres} {p.apellidos}")
        print(f"  Edad: {p.edad} | Sexo: {p.sexo} | Celular: {p.celular}")
        print(f"  Fecha de Atención: {fecha_str}")
        print(f"  Observaciones: {p.observaciones}")
    db.close()

if __name__ == "__main__":
    buscar_y_restaurar()
