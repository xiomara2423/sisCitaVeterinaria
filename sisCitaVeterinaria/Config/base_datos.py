import sqlite3

ARCHIVO_BD = "veterinaria.db"

def obtener_conexion():
    conn = sqlite3.connect(ARCHIVO_BD)
    #Acceder filas como diccionarios en lugar de tuplas
    conn.row_factory = sqlite3.Row
    #Aplicar integridad de llaves foraneas
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()

    #Tabla duenos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duenos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT UNIQUE,
            direccion TEXT NOT NULL,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    #Tabla mascotas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dueno_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            especie TEXT NOT NULL,
            raza TEXT,
            sexo TEXT CHECK (sexo IN ('M', 'H')),
            peso REAL,
            FOREIGN KEY (dueno_id) REFERENCES duenos(id)
        )
    """)

    #Tabla veterinarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            telefono TEXT,
            disponible INTEGER DEFAULT 1
        )
    """)

    #Tabla citas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota_id INTEGER NOT NULL,
            veterinario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            motivo TEXT NOT NULL,
            estado TEXT DEFAULT 'Programada' NOT NULL
                CHECK (estado IN ('Programada', 'Completada', 'Cancelada')),
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id),
            FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id)
        )
    """)

    conn.commit()
    conn.close()