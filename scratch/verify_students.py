import sys
import os
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona

db = SessionLocal()
for p_id in [42, 43, 214]:
    p = db.query(Persona).filter(Persona.id == p_id).first()
    if p:
        print(f"Estudiante ID {p.id}: {p.apellidos}, {p.nombres}")
        print(f"  Escuela ID: {p.escuela_id} | Escuela Nombre: {p.escuela.nombre if p.escuela else 'NINGUNA'}")
        print(f"  Facultad ID: {p.facultad_id} | Facultad Nombre: {p.facultad.nombre if p.facultad else 'NINGUNA'}")
    else:
        print(f"Estudiante ID {p_id} no encontrado.")

db.close()
