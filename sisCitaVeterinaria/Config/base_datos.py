import os 
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    
    #CREDENCIALES 
    conn = psycopg2.connect(
        host=os.getenv("BD_HOST", "localhost"),
        port=os.getenv("BD_PORT", "5432"),
        database=os.getenv("BD_NAME", "sistema_db"),
        user=os.getenv("BD_USER", "postgres"),
        password=os.getenv("BD_PASSWORD", "123456")
    )
    conn.cursor_factory=RealDictCursor
    return conn

def inicializar():
    # Crea las tablas si aún no existen en PostgreSQL
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla dueños
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duenos (
            id              SERIAL          PRIMARY KEY,
            nombre          TEXT            NOT NULL,
            apellido        TEXT            NOT NULL,
            telefono        TEXT            NOT NULL,
            email           TEXT            UNIQUE,
            direccion       TEXT            NOT NULL
        )
    """)

    # Tabla mascotas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id          SERIAL      PRIMARY KEY,
            dueno_id    INTEGER     NOT NULL,
            nombre      TEXT        NOT NULL,
            especie     TEXT        NOT NULL,
            raza        TEXT,
            sexo        TEXT        CHECK (sexo IN ('M', 'H')),
            peso        REAL,
            FOREIGN KEY (dueno_id) REFERENCES duenos(id)
        )
    """)

    # Tabla veterinarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veterinarios (
            id              SERIAL      PRIMARY KEY,
            nombre          TEXT        NOT NULL,
            apellido        TEXT        NOT NULL,
            especialidad    TEXT        NOT NULL,
            telefono        TEXT,
            disponible      BOOLEAN     DEFAULT TRUE
        )
    """)

    # Tabla citas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id              SERIAL      PRIMARY KEY,
            mascota_id      INTEGER     NOT NULL,
            veterinario_id  INTEGER     NOT NULL,
            fecha           TEXT        NOT NULL,
            motivo          TEXT        NOT NULL,
            estado          TEXT        DEFAULT 'Programada' NOT NULL
                                        CHECK (estado IN ('Programada', 'Completada', 'Cancelada')),
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id),
            FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id)
        )
    """)

    # Confirma y guarda los cambios en PostgreSQL
    conn.commit()
    conn.close()