import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import CatFacultad, CatEscuela, Persona

def corregir_estructura():
    db = SessionLocal()
    try:
        print("Iniciando corrección estructural de Medicina y Obstetricia...")
        
        # 1. Corregir nombre de la Facultad de Medicina
        fac_medicina_vieja = db.query(CatFacultad).filter(CatFacultad.nombre == "Medicina Humana y Odontología").first()
        fac_medicina_nueva = db.query(CatFacultad).filter(CatFacultad.nombre == "Medicina").first()
        
        if fac_medicina_vieja:
            if not fac_medicina_nueva:
                print(f"Renombrando facultad '{fac_medicina_vieja.nombre}' a 'Medicina'")
                fac_medicina_vieja.nombre = "Medicina"
                db.commit()
                fac_medicina_id = fac_medicina_vieja.id
            else:
                # Si por alguna razón ambas existen, migramos de la vieja a la nueva
                print(f"Fusionando facultad '{fac_medicina_vieja.nombre}' con la existente 'Medicina'")
                personas_afectadas = db.query(Persona).filter(Persona.facultad_id == fac_medicina_vieja.id).all()
                for p in personas_afectadas:
                    p.facultad_id = fac_medicina_nueva.id
                    
                escuelas_afectadas = db.query(CatEscuela).filter(CatEscuela.facultad_id == fac_medicina_vieja.id).all()
                for e in escuelas_afectadas:
                    e.facultad_id = fac_medicina_nueva.id
                
                db.delete(fac_medicina_vieja)
                db.commit()
                fac_medicina_id = fac_medicina_nueva.id
        elif fac_medicina_nueva:
            fac_medicina_id = fac_medicina_nueva.id
            print("La facultad 'Medicina' ya existe.")
        else:
            print("Creando nueva facultad 'Medicina'...")
            nueva_fac = CatFacultad(nombre="Medicina")
            db.add(nueva_fac)
            db.commit()
            fac_medicina_id = nueva_fac.id

        # 2. Asegurar que las escuelas Medicina Humana y Odontología pertenecen a la facultad de Medicina
        escuela_medicina = db.query(CatEscuela).filter(CatEscuela.nombre == "Medicina Humana").first()
        escuela_odontologia = db.query(CatEscuela).filter(CatEscuela.nombre == "Odontología").first()
        
        if escuela_medicina:
            if escuela_medicina.facultad_id != fac_medicina_id:
                print(f"Asignando escuela '{escuela_medicina.nombre}' a facultad 'Medicina'")
                escuela_medicina.facultad_id = fac_medicina_id
        else:
            print("Creando escuela 'Medicina Humana' bajo la facultad de 'Medicina'...")
            db.add(CatEscuela(nombre="Medicina Humana", facultad_id=fac_medicina_id))
            
        if escuela_odontologia:
            if escuela_odontologia.facultad_id != fac_medicina_id:
                print(f"Asignando escuela '{escuela_odontologia.nombre}' a facultad 'Medicina'")
                escuela_odontologia.facultad_id = fac_medicina_id
        else:
            print("Creando escuela 'Odontología' bajo la facultad de 'Medicina'...")
            db.add(CatEscuela(nombre="Odontología", facultad_id=fac_medicina_id))
            
        db.commit()

        # 3. Asegurar estructura de Obstetricia (Facultad Obstetricia -> Escuela Obstetricia)
        fac_obstetricia = db.query(CatFacultad).filter(CatFacultad.nombre == "Obstetricia").first()
        if not fac_obstetricia:
            print("Creando facultad 'Obstetricia'...")
            fac_obstetricia = CatFacultad(nombre="Obstetricia")
            db.add(fac_obstetricia)
            db.commit()
            
        escuela_obstetricia = db.query(CatEscuela).filter(CatEscuela.nombre == "Obstetricia").first()
        if escuela_obstetricia:
            if escuela_obstetricia.facultad_id != fac_obstetricia.id:
                print(f"Corrigiendo escuela 'Obstetricia': asignada a facultad 'Obstetricia' (ID: {fac_obstetricia.id})")
                escuela_obstetricia.facultad_id = fac_obstetricia.id
        else:
            print("Creando escuela 'Obstetricia' bajo la facultad 'Obstetricia'...")
            db.add(CatEscuela(nombre="Obstetricia", facultad_id=fac_obstetricia.id))
            
        db.commit()
        print("¡Corrección estructural completada exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al corregir base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    corregir_estructura()
