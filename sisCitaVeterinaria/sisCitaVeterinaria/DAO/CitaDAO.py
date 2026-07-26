from Config.logger import Logger
from Config.base_datos import obtener_conexion
from Modelos.Cita import Cita
from Config.sistema_config import CitaNoEncontradaError, EstadoInvalidoError

class CitaDAO:
    def __init__(self):
        self.__log = Logger()
    
    def insertar(self, cita):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO citas (mascota_id, veterinario_id, fecha, motivo, estado) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (cita.mascota_id, cita.veterinario_id, cita.fecha, cita.motivo, cita.estado)
        )
        cita.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Cita agregada: ID = {cita.id}")
        return cita
       
    def buscar_por_id(self, id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas WHERE id = %s", (id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cita(fila) if fila else None
    
    def obtener_todas(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas ORDER BY fecha DESC")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_cita(f) for f in filas]
    
    def actualizar(self, id, motivo=None, estado=None):
        c = self.buscar_por_id(id)
        if not c:
            raise CitaNoEncontradaError(id)
        if estado is not None and estado not in Cita.E_Validos:
            raise EstadoInvalidoError(estado)
        nuevo_motivo = motivo if motivo is not None else c.motivo
        nuevo_estado = estado if estado is not None else c.estado
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE citas SET motivo=%s, estado=%s WHERE id=%s",
            (nuevo_motivo, nuevo_estado, id)
        )
        conn.commit()
        conn.close()
        c.motivo = nuevo_motivo
        c.estado = nuevo_estado
        self.__log.info(f"Cita actualizada: ID = {id}")
        return c
    
    def eliminar(self, id):
        c = self.buscar_por_id(id)
        if not c:
            raise CitaNoEncontradaError(id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Cita eliminada: ID = {id}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM citas")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_cita(self, fila):
        c = Cita(fila["mascota_id"], fila["veterinario_id"], fila["fecha"], fila["motivo"], fila["estado"])
        c.id = fila["id"]
        return c
