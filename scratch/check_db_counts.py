from database.db_config import SessionLocal
from database.models import Atencion, CatCasoSocial, FichaSocioeconomica, Persona
from sqlalchemy import extract

db = SessionLocal()
try:
    print("=== INSPECCION DE ATENCIONES AGOSTO ===")
    atenciones_ago = db.query(Atencion).filter(
        Atencion.activo == True,
        extract('month', Atencion.fecha_atencion) == 8,
        extract('year', Atencion.fecha_atencion) == 2026
    ).all()
    
    print(f"Total atenciones activas en Agosto (2026): {len(atenciones_ago)}")
    
    # Ver distribución por CatCasoSocial
    conteo_casos = {}
    for a in atenciones_ago:
        caso_nom = a.caso_social.nombre if a.caso_social else "Sin Caso"
        conteo_casos[caso_nom] = conteo_casos.get(caso_nom, 0) + 1
        
    print("\n--- Distribucion por caso_social exacto ---")
    for nom, count in conteo_casos.items():
        print(f"'{nom}': {count}")
        
    print("\n--- Fichas Socioeconomicas ---")
    all_fichas = db.query(FichaSocioeconomica).count()
    print(f"Total fichas socioeconomicas en toda la BD: {all_fichas}")

finally:
    db.close()
