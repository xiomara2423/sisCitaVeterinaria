import psycopg2
from Config.logger import Logger
from Config.base_datos import obtener_conexion
from Modelos.Dueno import Dueno
from Config.sistema_config import DuenoNoEncontradoError, EmailDuplicadoError, DuenoConMascotasError

class DuenoDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_email(self, email):
        if not email:
            return None
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos WHERE email = %s", (email,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_dueno(fila) if fila else None

    def buscar_por_id(self, id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos WHERE id = %s", (id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_dueno(fila) if fila else None

    def insertar(self, dueno):
        # Verificar que el email no esté duplicado
        if dueno.email and self.buscar_por_email(dueno.email):
            self.__log.warning(f"Email duplicado: {dueno.email}")
            raise EmailDuplicadoError(dueno.email)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO duenos (nombre, apellido, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (dueno.nombre, dueno.apellido, dueno.telefono, dueno.email, dueno.direccion)
        )
        dueno.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Dueño agregado: {dueno.nombre} {dueno.apellido} (ID = {dueno.id})")
        return dueno

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_dueno(f) for f in filas]

    def actualizar(self, id, nombre=None, apellido=None, telefono=None, email=None, direccion=None):
        d = self.buscar_por_id(id)
        if not d:
            self.__log.error(f"Actualizar fallido: Dueño ID = {id} no existe")
            raise DuenoNoEncontradoError(id)
        # Validar email
        if email and email != d.email and self.buscar_por_email(email):
            self.__log.warning(f"Actualizar fallido: Email duplicado")
            raise EmailDuplicadoError(email)
        nuevo_nombre = nombre if nombre is not None else d.nombre
        nuevo_apellido = apellido if apellido is not None else d.apellido
        nuevo_telefono = telefono if telefono is not None else d.telefono
        nuevo_email = email if email is not None else d.email
        nueva_direccion = direccion if direccion is not None else d.direccion

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE duenos SET nombre=%s, apellido=%s, telefono=%s, email=%s, direccion=%s WHERE id=%s""",
            (nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, nueva_direccion, id)
        )
        conn.commit()
        conn.close()
        d.nombre = nuevo_nombre
        d.apellido = nuevo_apellido
        d.telefono = nuevo_telefono
        d.email = nuevo_email
        d.direccion = nueva_direccion

        self.__log.info(f"Dueño actualizado: ID = {id}")
        return d

    def eliminar(self, id):
        d = self.buscar_por_id(id)
        if not d:
            self.__log.error(f"Eliminar fallido: Dueño ID = {id} no existe")
            raise DuenoNoEncontradoError(id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM duenos WHERE id = %s", (id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Dueño ID = {id} tiene mascotas registradas")
            raise DuenoConMascotasError(id)
        conn.close()
        self.__log.info(f"Dueño eliminado: {d.nombre} {d.apellido} (ID = {id})")
        return True
# metodo contador de registros
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM duenos")
        total = cursor.fetchone()["total"]
        conn.close()
        return total
 
    def __fila_a_dueno(self, fila):
        d = Dueno(fila["nombre"], fila["apellido"], fila["telefono"], fila["email"], fila["direccion"])
        d.id = fila["id"]
        return d