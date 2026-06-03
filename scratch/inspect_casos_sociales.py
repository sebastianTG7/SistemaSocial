import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import CatCasoSocial

def inspect():
    db = SessionLocal()
    try:
        casos = db.query(CatCasoSocial).all()
        print(f"Total Casos Sociales: {len(casos)}")
        for c in casos:
            print(f"ID: {c.id} | Nombre: {c.nombre} | Activo: {c.activo}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect()
