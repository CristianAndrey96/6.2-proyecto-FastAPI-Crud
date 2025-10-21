from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL DE LA BASE DE DATOS SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./carros.db"

#Crear el motor de conexion
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Crear Sesion y base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


