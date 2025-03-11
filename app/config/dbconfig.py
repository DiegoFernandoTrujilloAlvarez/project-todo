from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

print("DB name")
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear una sesión de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir modelos
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
