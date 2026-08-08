-- Tabla dueños
CREATE TABLE IF NOT EXISTS duenos (
    id              SERIAL          PRIMARY KEY,
    nombre          TEXT            NOT NULL,
    apellido        TEXT            NOT NULL,
    telefono        TEXT            NOT NULL,
    email           TEXT            UNIQUE NOT NULL,
    direccion       TEXT            NOT NULL
);

-- Tabla mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id          SERIAL      PRIMARY KEY,
    dueno_id    INTEGER     NOT NULL,
    nombre      TEXT        NOT NULL,
    especie     TEXT        NOT NULL,
    raza        TEXT,
    sexo        TEXT        CHECK (sexo IN ('M', 'H')),
    peso        NUMERIC (5,2),
    FOREIGN KEY (dueno_id) REFERENCES duenos(id)
);

-- Tabla veterinarios
CREATE TABLE IF NOT EXISTS veterinarios (
    id              SERIAL      PRIMARY KEY,
    nombre          TEXT        NOT NULL,
    apellido        TEXT        NOT NULL,
    especialidad    TEXT        NOT NULL,
    telefono        TEXT		NOT NULL,
    disponible      BOOLEAN     DEFAULT TRUE
);

-- Tabla citas
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
);

INSERT INTO duenos (nombre, apellido, telefono, email, direccion) VALUES
    ('Juan',  'Perez',  '987654321', 'juanperez@gmail.com',  'av las Paltas 505'),
    ('Maria', 'Nuñez',  '987654322', 'marianunez@gmail.com', 'av las Peras 556');

INSERT INTO veterinarios (nombre, apellido, especialidad, telefono) VALUES
    ('Anthonio', 'Vasquez', 'Oftalmologo', '987654334'),
    ('Laura',    'Roca',    'Cirujana',    '983654334');

INSERT INTO mascotas (dueno_id, nombre, especie, raza, sexo, peso) VALUES
    (1, 'Poli', 'Perro', 'Mestizo', 'H', 15),
    (2, 'Roco', 'Gato',  'Mestizo', 'M', 8);

INSERT INTO citas (mascota_id, veterinario_id, fecha, motivo) VALUES
    (1, 1, '2026-04-01 08:30:00', 'Chequeo visual'),
    (2, 2, '2026-06-01 10:00:00', 'Cirugia gastrica');

SELECT 'duenos'       AS tabla, COUNT(*) AS registros FROM duenos
UNION ALL
SELECT 'mascotas'     AS tabla, COUNT(*) AS registros FROM mascotas
UNION ALL
SELECT 'veterinarios' AS tabla, COUNT(*) AS registros FROM veterinarios
UNION ALL
SELECT 'citas'        AS tabla, COUNT(*) AS registros FROM citas;