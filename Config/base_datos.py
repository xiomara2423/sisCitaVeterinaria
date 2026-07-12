import sqlite3

# Nombre del archivo de base de datos SQLite.
# SQLite guarda toda la base de datos en un solo archivo .db en el disco,
# lo que lo hace ideal para aprender: no requiere instalar ningún servidor.
ARCHIVO_BD = "veterinaria.db"


def obtener_conexion():
    # sqlite3.connect() abre (o crea si no existe) el archivo de base de datos.
    conn = sqlite3.connect(ARCHIVO_BD)
    # row_factory = sqlite3.Row hace que cada fila se pueda acceder como diccionario:
    # fila["nombre"] en lugar de fila[1]. Es mucho más legible y menos propenso a errores.
    conn.row_factory = sqlite3.Row
    # PRAGMA foreign_keys activa la validación de FOREIGN KEY, que SQLite trae
    # desactivada por defecto. Sin esto, las FOREIGN KEY de abajo no se harían cumplir.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar():
    # Crea las tablas si aún no existen. Se llama UNA vez al iniciar el sistema.
    # "IF NOT EXISTS" evita un error si la tabla ya fue creada en una ejecución anterior.
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla de dueños: email tiene restricción UNIQUE para evitar duplicados a nivel de BD
    # (la misma regla que ya valida DuenoDAO en memoria, pero reforzada por el motor).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duenos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT UNIQUE,
            direccion TEXT,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de mascotas: tiene FOREIGN KEY que enlaza con duenos.
    # FOREIGN KEY garantiza integridad referencial: no se puede registrar una mascota
    # con un dueno_id que no exista en la tabla duenos.
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            especialidad TEXT,
            telefono TEXT,
            disponible INTEGER DEFAULT 1
        )
    """)

    # Tabla de citas: tiene FOREIGN KEY que enlaza con mascotas y veterinarios.
    # No se puede registrar una cita con un mascota_id o veterinario_id que no exista
    # en sus tablas respectivas — la misma protección que MascotaNoEncontradaError y
    # VeterinarioNoEncontradoError ya dan en memoria, ahora también a nivel de BD.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota_id INTEGER NOT NULL,
            veterinario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            motivo TEXT NOT NULL,
            estado TEXT DEFAULT 'Programada'
                CHECK (estado IN ('Programada', 'Completada', 'Cancelada')),
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id),
            FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id)
        )
    """)

    # conn.commit() confirma todos los cambios (equivale a "guardar" en la BD).
    # Sin commit(), los cambios se pierden al cerrar la conexión.
    conn.commit()
    conn.close()