import bcrypt
from database.db_config import engine, SessionLocal, Base
from database.models import User, CatTipoUsuario, CatCasoSocial, CatFacultad, CatEscuela

# Datos reales de la universidad
FACULTADES_ESCUELAS = {
    "Ciencias Agrarias": [
        "Ingeniería Agronómica",
        "Ingeniería Agroindustrial",
    ],
    "Medicina": [
        "Medicina Humana",
        "Odontología",
    ],
    "Psicología": [
        "Psicología",
    ],
    "Enfermería": [
        "Enfermería",
    ],
    "Obstetricia": [
        "Obstetricia",
    ],
    "Ciencias Administrativas y Turismo": [
        "Ciencias Administrativas",
        "Turismo y Hotelería",
    ],
    "Ciencias Contables y Financieras": [
        "Ciencias Contables y Financieras",
    ],
    "Economía": [
        "Economía",
    ],
    "Ciencias Sociales": [
        "Ciencias de la Comunicación Social",
        "Sociología",
    ],
    "Ciencias de la Educación": [
        "Educación Inicial",
        "Educación Primaria",
        "Educación Física",
        "Biología, Química y Ciencia del Ambiente",
        "Ciencias Histórico Sociales y Geográficas",
        "Filosofía, Psicología y Ciencias Sociales",
        "Lengua y Literatura",
        "Matemática y Física",
    ],
    "Derecho y Ciencias Políticas": [
        "Derecho y Ciencias Políticas",
    ],
    "Ingeniería Civil y Arquitectura": [
        "Ingeniería Civil",
        "Arquitectura",
    ],
    "Ingeniería Industrial, de Sistemas y Mecatrónica": [
        "Ingeniería Industrial",
        "Ingeniería de Sistemas",
        "Ingeniería Mecatrónica",
    ],
    "Medicina Veterinaria y Zootecnia": [
        "Medicina Veterinaria",
    ],
}


def init_db():
    # Crear todas las tablas (para DBs nuevas)
    Base.metadata.create_all(bind=engine)

    # ── Migración: agregar columna 'cargo' si no existe ─────────────────────
    from sqlalchemy import text, inspect
    with engine.connect() as conn:
        inspector = inspect(engine)
        columnas = [col["name"] for col in inspector.get_columns("usuarios")]
        if "cargo" not in columnas:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN cargo VARCHAR(100)"))
            conn.commit()
            print("  [OK] Migracion: columna 'cargo' agregada a la tabla 'usuarios'.")

    db = SessionLocal()

    # 1. Usuario administrador por defecto
    if db.query(User).filter(User.username == "admin").first() is None:
        hashed_password = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
        admin_user = User(
            username="admin",
            password_hash=hashed_password.decode("utf-8"),
            nombre_completo="Administrador del Sistema",
            cargo="Administrador",
            rol="administrador",
        )
        db.add(admin_user)
        print("  [OK] Usuario 'admin' creado (Pass: admin123).")

    # 1b. Usuario operador por defecto
    if db.query(User).filter(User.username == "neri").first() is None:
        hashed_neri = bcrypt.hashpw("19604085".encode("utf-8"), bcrypt.gensalt())
        neri_user = User(
            username="neri",
            password_hash=hashed_neri.decode("utf-8"),
            nombre_completo="Neri",
            cargo="Trabajadora Social",
            rol="operador",
        )
        db.add(neri_user)
        print("  [OK] Usuario 'neri' creado (operador).")

    # 2. Tipos de usuario
    if db.query(CatTipoUsuario).count() == 0:
        tipos = [CatTipoUsuario(nombre="Estudiante"), CatTipoUsuario(nombre="Egresado")]
        db.add_all(tipos)
        print("  [OK] Catálogo Tipos de Usuario inicializado.")

    # 3. Casos sociales
    if db.query(CatCasoSocial).count() == 0:
        casos = [
            CatCasoSocial(nombre="Orientación"),
            CatCasoSocial(nombre="Seguimiento"),
            CatCasoSocial(nombre="Monitoreo"),
            CatCasoSocial(nombre="Derivación"),
        ]
        db.add_all(casos)
        print("  [OK] Catálogo Casos Sociales inicializado.")

    # 4. Facultades y Escuelas reales
    if db.query(CatFacultad).count() == 0:
        for nombre_facultad, escuelas in FACULTADES_ESCUELAS.items():
            facultad = CatFacultad(nombre=nombre_facultad)
            db.add(facultad)
            db.flush()  # Obtener el ID sin hacer commit
            for nombre_escuela in escuelas:
                escuela = CatEscuela(nombre=nombre_escuela, facultad_id=facultad.id)
                db.add(escuela)
        print(f"  [OK] {len(FACULTADES_ESCUELAS)} Facultades y sus Escuelas inicializadas.")

    db.commit()
    db.close()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()
