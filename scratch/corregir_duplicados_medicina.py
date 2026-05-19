import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import CatEscuela, Persona

def limpiar_duplicados_medicina():
    db = SessionLocal()
    try:
        print("Iniciando depuración de duplicados de Medicina Humana, Odontología y Obstetricia...")
        
        # 1. Corregir Medicina Humana (mantener ID: 3, borrar ID: 33)
        escuela_mh_mantener = db.query(CatEscuela).filter(CatEscuela.id == 3).first()
        escuela_mh_borrar = db.query(CatEscuela).filter(CatEscuela.id == 33).first()
        
        if escuela_mh_borrar and escuela_mh_mantener:
            personas_mh = db.query(Persona).filter(Persona.escuela_id == 33).all()
            if personas_mh:
                print(f"Redireccionando {len(personas_mh)} personas de Medicina Humana (ID: 33) a (ID: 3)")
                for p in personas_mh:
                    p.escuela_id = 3
            print("Eliminando escuela duplicada 'Medicina Humana' (ID: 33)")
            db.delete(escuela_mh_borrar)
        
        # 2. Corregir Odontología (mantener ID: 4, borrar ID: 32)
        escuela_od_mantener = db.query(CatEscuela).filter(CatEscuela.id == 4).first()
        escuela_od_borrar = db.query(CatEscuela).filter(CatEscuela.id == 32).first()
        
        if escuela_od_borrar and escuela_od_mantener:
            personas_od = db.query(Persona).filter(Persona.escuela_id == 32).all()
            if personas_od:
                print(f"Redireccionando {len(personas_od)} personas de Odontología (ID: 32) a (ID: 4)")
                for p in personas_od:
                    p.escuela_id = 4
            print("Eliminando escuela duplicada 'Odontología' (ID: 32)")
            db.delete(escuela_od_borrar)
            
        # 3. Corregir Obstetricia de Medicina (mantener ID: 7 en Facultad Obstetricia, borrar ID: 34 en Facultad Medicina)
        escuela_obs_mantener = db.query(CatEscuela).filter(CatEscuela.id == 7).first()
        escuela_obs_borrar = db.query(CatEscuela).filter(CatEscuela.id == 34).first()
        
        if escuela_obs_borrar and escuela_obs_mantener:
            personas_obs = db.query(Persona).filter(Persona.escuela_id == 34).all()
            if personas_obs:
                print(f"Redireccionando {len(personas_obs)} personas de Obstetricia de Medicina (ID: 34) a Obstetricia de Obstetricia (ID: 7)")
                for p in personas_obs:
                    p.escuela_id = 7
            print("Eliminando escuela incorrecta 'Obstetricia' bajo Medicina (ID: 34)")
            db.delete(escuela_obs_borrar)

        db.commit()
        print("¡Limpieza de duplicados de Medicina y Obstetricia completada exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al limpiar duplicados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_duplicados_medicina()
