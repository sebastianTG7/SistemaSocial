import sys
import os
sys.path.append(os.getcwd())

from database.db_config import SessionLocal
from database.models import Persona

db = SessionLocal()
students = db.query(Persona).filter(Persona.escuela_id == 17).all()
print(f"Total students with escuela_id == 17: {len(students)}")
for s in students:
    print(f"ID: {s.id} | Name: {s.apellidos}, {s.nombres} | Active: {s.activo}")
db.close()
