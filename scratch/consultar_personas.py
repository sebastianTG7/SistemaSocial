import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona, CatEscuela, CatFacultad

def consultar_todas():
    db = SessionLocal()
    try:
        personas = db.query(Persona).all()
        print(f"--- TOTAL DE PERSONAS EN BASE DE DATOS: {len(personas)} ---")
        for p in personas:
            escuela_nombre = p.escuela.nombre if p.escuela else "Sin Escuela"
            facultad_nombre = p.facultad.nombre if p.facultad else "Sin Facultad"
            # Formatear la fecha
            fecha_str = p.fecha_atencion.strftime("%Y-%m-%d") if p.fecha_atencion else "Sin Fecha"
            print(f"ID: {p.id} | DNI: {p.dni} | Nombre: {p.nombres} {p.apellidos} | Facultad: {facultad_nombre} | Escuela: {escuela_nombre} | Fecha: {fecha_str} | Semestre: {p.año_estudio} | Celular: {p.celular}")
    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    consultar_todas()
