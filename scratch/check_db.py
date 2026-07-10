import sys
import os
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import CatFacultad, CatEscuela, Persona

db = SessionLocal()
total_personas = db.query(Persona).count()
print(f"Total personas en la base de datos: {total_personas}")

print("\n=== Personas por Facultad ===")
for f in db.query(CatFacultad).all():
    c = db.query(Persona).filter(Persona.facultad_id == f.id).count()
    if c > 0:
        print(f"Facultad ID {f.id}: '{f.nombre}' -> {c} personas")

print("\n=== Personas por Escuela ===")
for e in db.query(CatEscuela).all():
    c = db.query(Persona).filter(Persona.escuela_id == e.id).count()
    if c > 0:
        print(f"Escuela ID {e.id}: '{e.nombre}' -> {c} personas")

# Check if there are any other schools with communication or biology/chemistry in name
print("\n=== Busqueda por texto en Escuela ===")
for e in db.query(CatEscuela).all():
    if "comunic" in e.nombre.lower() or "biolog" in e.nombre.lower() or "quim" in e.nombre.lower():
         c = db.query(Persona).filter(Persona.escuela_id == e.id).count()
         print(f"Escuela ID {e.id}: '{e.nombre}' (Facultad: '{e.facultad.nombre}') -> {c} personas")

db.close()
