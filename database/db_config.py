from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ruta de la base de datos (SQLite)
DB_PATH = "database/servicio_social.db"
DB_URL = f"sqlite:///{DB_PATH}"

# Configuración de SQLAlchemy
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
