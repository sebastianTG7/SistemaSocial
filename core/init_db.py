import bcrypt
from database.db_config import engine, SessionLocal, Base
from database.models import User, CatTipoUsuario, CatCasoSocial, CatFacultad, CatEscuela

# Datos reales de la universidad
FACULTADES_ESCUELAS = {
    "Ciencias Agrarias": [
        "Ingeniería Agronómica",
        "Ingeniería Agroindustrial",
    ],
    "Medicina Humana y Odontología": [
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
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # 1. Usuario administrador por defecto
    if db.query(User).filter(User.username == "admin").first() is None:
        hashed_password = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
        admin_user = User(
            username="admin",
            password_hash=hashed_password.decode("utf-8"),
            nombre_completo="Administrador del Sistema",
            rol="administrador",
        )
        db.add(admin_user)
        print("  ✔ Usuario 'admin' creado (Pass: admin123).")

    # 2. Tipos de usuario
    if db.query(CatTipoUsuario).count() == 0:
        tipos = [CatTipoUsuario(nombre="Alumno"), CatTipoUsuario(nombre="Egresado")]
        db.add_all(tipos)
        print("  ✔ Catálogo Tipos de Usuario inicializado.")

    # 3. Casos sociales
    if db.query(CatCasoSocial).count() == 0:
        casos = [
            CatCasoSocial(nombre="Orientación"),
            CatCasoSocial(nombre="Seguimiento"),
            CatCasoSocial(nombre="Monitoreo"),
        ]
        db.add_all(casos)
        print("  ✔ Catálogo Casos Sociales inicializado.")

    # 4. Facultades y Escuelas reales
    if db.query(CatFacultad).count() == 0:
        for nombre_facultad, escuelas in FACULTADES_ESCUELAS.items():
            facultad = CatFacultad(nombre=nombre_facultad)
            db.add(facultad)
            db.flush()  # Obtener el ID sin hacer commit
            for nombre_escuela in escuelas:
                escuela = CatEscuela(nombre=nombre_escuela, facultad_id=facultad.id)
                db.add(escuela)
        print(f"  ✔ {len(FACULTADES_ESCUELAS)} Facultades y sus Escuelas inicializadas.")

    db.commit()
    db.close()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()
