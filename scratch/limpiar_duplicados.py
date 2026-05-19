import os
import sys

# Añadir el directorio raíz al path de Python para poder importar core y database
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import CatEscuela, Persona

def limpiar_duplicados():
    db = SessionLocal()
    try:
        print("Buscando escuelas a eliminar...")
        
        # 1. Buscar las escuelas que se quieren mantener y las que se quieren borrar
        escuela_historico_mantener = db.query(CatEscuela).filter(CatEscuela.nombre == "Ciencias Historico Sociales y Geográficas").first()
        escuela_historico_borrar = db.query(CatEscuela).filter(CatEscuela.nombre == "Ciencias Histórico Sociales y Geográficas").first()
        
        escuela_lengua_mantener = db.query(CatEscuela).filter(CatEscuela.nombre == "Lengua y Literatura").first()
        escuela_lenguaje_borrar = db.query(CatEscuela).filter(CatEscuela.nombre == "Lenguaje y Literatura").first()
        
        # 2. Migrar registros de 'Personas' si es que alguno estuviera apuntando a la escuela que se va a borrar
        if escuela_historico_borrar and escuela_historico_mantener:
            personas_afectadas = db.query(Persona).filter(Persona.escuela_id == escuela_historico_borrar.id).all()
            if personas_afectadas:
                print(f"Redirigiendo {len(personas_afectadas)} personas de 'Ciencias Histórico...' a 'Ciencias Historico...'")
                for p in personas_afectadas:
                    p.escuela_id = escuela_historico_mantener.id
            
            print(f"Eliminando escuela duplicada: '{escuela_historico_borrar.nombre}' (ID: {escuela_historico_borrar.id})")
            db.delete(escuela_historico_borrar)
        else:
            print("No se encontró duplicado para 'Ciencias Histórico Sociales y Geográficas' o ya fue eliminado.")
            
        if escuela_lenguaje_borrar and escuela_lengua_mantener:
            personas_afectadas = db.query(Persona).filter(Persona.escuela_id == escuela_lenguaje_borrar.id).all()
            if personas_afectadas:
                print(f"Redirigiendo {len(personas_afectadas)} personas de 'Lenguaje y Literatura' a 'Lengua y Literatura'")
                for p in personas_afectadas:
                    p.escuela_id = escuela_lengua_mantener.id
                    
            print(f"Eliminando escuela duplicada: '{escuela_lenguaje_borrar.nombre}' (ID: {escuela_lenguaje_borrar.id})")
            db.delete(escuela_lenguaje_borrar)
        else:
            print("No se encontró duplicado para 'Lenguaje y Literatura' o ya fue eliminado.")
            
        db.commit()
        print("¡Limpieza de base de datos completada exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al limpiar base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_duplicados()
