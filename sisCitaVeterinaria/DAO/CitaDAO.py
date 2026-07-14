from Config.logger import Logger
from Modelos.Cita import Cita

class CitaNoEncontradaError(Exception):
    def __init__(self, id): super().__init__(f"Cita ID = {id} no encontrada")
    
class EstadoInvalidoError(Exception):
    def __init__(self, estado, validos):
        super().__init__(f"Estado inválido '{estado}'. Use uno de: {validos}")

class CitaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, id):
        for c in self.__bd:
            if c.id == id:
                return c
        return None

    def insertar(self, cita):
        cita.id = self.__cid
        self.__cid += 1
        self.__bd.append(cita)
        self.__log.info(f"Cita agendada: ID = {cita.id}")
        return cita

    def obtener_todas(self):
        return sorted(self.__bd, key=lambda c: c.fecha)

    def cambiar_estado(self, id, nuevo_estado):
        c = self.buscar_por_id(id)
        if not c:
            self.__log.error(f"Actualizar fallido: Cita ID = {id} no existe")
            raise CitaNoEncontradaError(id)
        if nuevo_estado not in Cita.E_Validos:
            raise EstadoInvalidoError(nuevo_estado, Cita.E_Validos)
        c.estado = nuevo_estado
        self.__log.info(f"Cita ID = {id} | Estado = {nuevo_estado}")
        return c

    def eliminar(self, id):
        c = self.buscar_por_id(id)
        if not c:
            self.__log.error(f"Eliminar fallido: Cita ID = {id} no existe")
            raise CitaNoEncontradaError(id)
        self.__bd.remove(c)
        self.__log.info(f"Cita eliminada: ID = {id}")
        return True

    def total(self):
        return len(self.__bd)