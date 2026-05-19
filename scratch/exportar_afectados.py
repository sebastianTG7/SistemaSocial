import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona, CatEscuela, CatFacultad

def exportar_registros_afectados():
    db = SessionLocal()
    try:
        # Buscar todas las personas que no tienen escuela asignada o pertenecen a Medicina/Obstetricia
        personas = db.query(Persona).all()
        print("=== INVENTARIO DE REGISTROS DE MEDICINA, OBSTETRICIA O CON 'SIN ESCUELA' ===")
        for p in personas:
            escuela_nombre = p.escuela.nombre if p.escuela else None
            facultad_nombre = p.facultad.nombre if p.facultad else "Sin Facultad"
            
            # Filtrar para mostrar solo los de interés:
            # - Facultad es Medicina u Obstetricia
            # - O bien, Escuela es NULL (Sin Escuela)
            es_interesante = (
                "medicina" in facultad_nombre.lower() or 
                "obstetricia" in facultad_nombre.lower() or 
                escuela_nombre is None
            )
            
            if es_interesante:
                fecha_str = p.fecha_atencion.strftime("%Y-%m-%d") if p.fecha_atencion else "Sin Fecha"
                print(f"ID: {p.id}")
                print(f"  DNI: {p.dni}")
                print(f"  Nombre Completo: {p.nombres} {p.apellidos}")
                print(f"  Edad: {p.edad} | Sexo: {p.sexo}")
                print(f"  Celular: {p.celular} | Correo: {p.correo}")
                print(f"  Facultad: {facultad_nombre} (ID: {p.facultad_id})")
                print(f"  Escuela: {escuela_nombre if escuela_nombre else 'SIN ESCUELA'} (ID original en DB: {p.escuela_id})")
                print(f"  Fecha de Atención: {fecha_str}")
                print(f"  Observaciones: {p.observaciones}")
                print("-" * 60)
    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    exportar_registros_afectados();
