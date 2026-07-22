import psycopg2
from Config.base_datos import obtener_conexion
from Config.logger import Logger
from Config.sistema_config import VeterinarioNoEncontradoError, VeterinarioConCitasError
from Modelos.Veterinario import Veterinario

class VeterinarioDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, veterinario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO veterinarios (nombre, apellido, especialidad, telefono, disponible) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (veterinario.nombre, veterinario.apellido, veterinario.especialidad, veterinario.telefono, veterinario.disponible)
        )
        veterinario.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Veterinario agregado: {veterinario.nombre} {veterinario.apellido} (ID = {veterinario.id})")
        return veterinario
    
    def buscar_por_id(self, id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM veterinarios WHERE id = %s", (id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_veterinario(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM veterinarios ORDER BY nombre ASC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_veterinario(f) for f in filas]

    def actualizar(self, id, nombre=None, apellido=None, especialidad=None, telefono=None, disponible=None):
        v = self.buscar_por_id(id)
        if not v:
            self.__log.error(f"Actualizar fallido: Veterinario ID = {id} no existe")
            raise VeterinarioNoEncontradoError(id)
        nuevo_nombre = nombre if nombre is not None else v.nombre
        nuevo_apellido = apellido if apellido is not None else v.apellido
        nuevo_espec = especialidad if especialidad is not None else v.especialidad
        nuevo_telef = telefono if telefono is not None else v.telefono
        nuevo_disponible = disponible if disponible is not None else v.disponible
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE veterinarios SET nombre = %s, apellido = %s, especialidad = %s, telefono = %s, disponible = %s WHERE id = %s",
            (nuevo_nombre, nuevo_apellido, nuevo_espec, nuevo_telef, nuevo_disponible, id)
        )
        conn.commit()
        conn.close()
        v.nombre = nuevo_nombre
        v.apellido = nuevo_apellido
        v.especialidad = nuevo_espec
        v.telefono = nuevo_telef
        v.disponible = nuevo_disponible
        self.__log.info(f"Veterinario actualizado: ID = {id}")
        return v

    def eliminar(self, id):
        v = self.buscar_por_id(id)
        if not v:
            self.__log.error(f"Eliminar fallido: Veterinario ID = {id} no existe")
            raise VeterinarioNoEncontradoError(id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM veterinarios WHERE id = %s", (id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Veterinario ID = {id} tiene citas asociadas")
            raise VeterinarioConCitasError(id)
        conn.close()
        self.__log.info(f"Veterinario eliminado: ID = {id}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM veterinarios")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_veterinario(self, fila):
        v = Veterinario(fila["nombre"], fila["apellido"], fila["especialidad"], fila["telefono"], fila["disponible"])
        v.id = fila["id"]
        return v
