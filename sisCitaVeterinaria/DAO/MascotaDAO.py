import sqlite3
from Config.logger import Logger
from Config.base_datos import obtener_conexion
from Config.sistema_config import MascotaNoEncontradaError, MascotaConCitasError
from Modelos.Mascota import Mascota


class MascotaDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, mascota):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mascotas (dueno_id, nombre, especie, raza, sexo, peso) VALUES (?, ?, ?, ?, ?, ?)",
            (mascota.dueno_id, mascota.nombre, mascota.especie, mascota.raza, mascota.sexo, mascota.peso)
        ) 
        # Aplicar cambios
        conn.commit()
        mascota.id = cursor.lastrowid
        conn.close()
        self.__log.info(f"Mascota agregada: {mascota.nombre} (ID = {mascota.id})")
        return mascota

    def buscar_por_id(self, id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mascotas WHERE id = ?", (id,))
        fila = cursor.fetchone()
        conn.close()
        # retorna el registro del metodo __fila_a_mascota a traves de su "id"
        return self.__fila_a_mascota(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mascotas ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        # retorna los registros del metodo __fila_a_mascota
        return [self.__fila_a_mascota(f) for f in filas]

    def eliminar(self, id):
        m = self.buscar_por_id(id)
        
        if not m:
            self.__log.error(f"Eliminar fallido: Mascota ID = {id} no existe")
            raise MascotaNoEncontradaError(id)
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM mascotas WHERE id = ?", (id,))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Mascota ID = {id} tiene citas asociadas")
            raise MascotaConCitasError(id)
            
        conn.close()
        self.__log.info(f"Mascota eliminada: {m.nombre} (ID = {id})")
        return True


    def actualizar(self, id, nombre=None, raza=None, peso=None):
        m = self.buscar_por_id(id)
        if not m:
            raise MascotaNoEncontradaError(id)
        
        nuevo_nombre = nombre if nombre is not None else m.nombre
        nueva_raza = raza if raza is not None else m.raza
        nuevo_peso = peso if peso is not None else m.peso

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE mascotas SET nombre=?, raza=?, peso=? WHERE id=?",
            (nuevo_nombre, nueva_raza, nuevo_peso, id)
        )
        conn.commit()
        conn.close()
        
        m.nombre = nuevo_nombre
        m.raza = nueva_raza
        m.peso = nuevo_peso
        return m

    def __fila_a_mascota(self, fila):
        m = Mascota(fila["dueno_id"], fila["nombre"], fila["especie"], fila["raza"], fila["sexo"], fila["peso"])
        m.id = fila["id"]
        return m
