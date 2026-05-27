import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.getcwd())

from controllers.persona_controller import PersonaController

def inspect():
    p_all = PersonaController.get_all(solo_activos=False)
    print(f"Total records returned: {len(p_all)}")
    
    active_count = sum(1 for p in p_all if p["activo"])
    inactive_count = sum(1 for p in p_all if not p["activo"])
    
    print(f"Active records (p['activo'] is True/truthy): {active_count}")
    print(f"Inactive records (p['activo'] is False/falsy): {inactive_count}")
    
    print("\nSample inactive records (first 5):")
    inactives = [p for p in p_all if not p["activo"]]
    for p in inactives[:5]:
        print(f"ID: {p['id']} | DNI: {p['dni']} | Nombre: {p['apellidos']}, {p['nombres']} | Activo: {p['activo']}")

if __name__ == "__main__":
    inspect()
