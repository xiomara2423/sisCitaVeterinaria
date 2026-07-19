import sqlite3
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
        #llamando la conexion del sql
        conn = obtener_conexion()
        #ejecuta las ordenes, ejem("SELECT")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos WHERE email = ?", (email.strip().lower(),))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_dueno(fila) if fila else None

    def buscar_por_id(self, id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos WHERE id = ?", (id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_dueno(fila) if fila else None

    def insertar(self, dueno):
        if dueno.email and self.buscar_por_email(dueno.email):
            self.__log.warning(f"Email duplicado: {dueno.email}")
            raise EmailDuplicadoError(dueno.email)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO duenos (nombre, apellido, telefono, email, direccion) VALUES (?, ?, ?, ?, ?)",
            (dueno.nombre, dueno.apellido, dueno.telefono, dueno.email, dueno.direccion)
            )
        conn.commit()
        
        #Asigna el id generado por SQLite al nuevo registro
        dueno.id = cursor.lastrowid
        conn.close()

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM duenos ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_dueno(f) for f in filas]

    def actualizar(self, id, nombre=None, telefono=None, email=None, direccion=None):
        d = self.buscar_por_id(id)
        if not d:
            self.__log.error(f"Actualizar fallido: Dueño ID = {id} no existe")
            raise DuenoNoEncontradoError(id)
        
        if email:
            email = email.strip().lower()
            if email != d.email and self.buscar_por_email(email):
                raise EmailDuplicadoError(email)
     #"nuevo_*" almacena los datos asignados por teclado, en caso no se actualice , 
     # el nombre anterior pasa a ser el actual
        nuevo_nombre = nombre if nombre is not None else d.nombre
        nuevo_telefono = telefono if telefono is not None else d.telefono
        nuevo_email = email if email is not None else d.email
        nuevo_direccion = direccion if direccion is not None else d.direccion
    
        conn = obtener_conexion()
        cursor = conn.cursor()
        # 
        cursor.execute(
            "UPDATE duenos SET nombre=?, telefono=?, email=?, direccion=? WHERE id=?",
            (nuevo_nombre, nuevo_telefono, nuevo_email, nuevo_direccion, id)
            )
        conn.commit()
        conn.close()
        d.nombre = nuevo_nombre
        d.telefono = nuevo_telefono
        d.email = nuevo_email
        d.direccion = nuevo_direccion
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
            cursor.execute("DELETE FROM duenos WHERE id = ?", (id,))
            conn.commit()
        except sqlite3.IntegrityError:
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
        cursor.execute("SELECT COUNT(*) FROM duenos")
        #le pide el resultado de cuantos registros hay ejem "[2]"
        total = cursor.fetchone()[0]
        conn.close()
        return total
 
    def __fila_a_dueno(self, fila):
       # los campos de la tabla dueño se almacena en el objeto ("d") 
        d = Dueno(fila["nombre"], fila["apellido"], fila["telefono"], fila["email"], fila["direccion"])
      
        # el objeto "d" y su atributo "id"
        d.id = fila["id"]
        return d