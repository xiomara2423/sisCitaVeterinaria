from Config.logger import Logger

class MascotaNoEncontradaError(Exception):
    def __init__(self, id): super().__init__(f"Mascota ID = {id} no encontrada")
    
class MascotaDAO:
    def __init__(self):
        self.__bd = []
        self.__mid = 1
        self.__log = Logger()

    def buscar_por_id(self, id):
        for m in self.__bd:
            if m.id == id:
                return m
        return None

    def buscar_por_dueno(self, dueno_id):
        return [m for m in self.__bd if m.dueno_id == dueno_id]

    def insertar(self, mascota):
        mascota.id = self.__mid
        self.__mid += 1
        self.__bd.append(mascota)
        self.__log.info(f"Mascota agregada: {mascota.nombre} (ID = {mascota.id})")
        return mascota

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda m: m.nombre)

    def actualizar(self, id, nombre=None, raza=None, peso=None):
        m = self.buscar_por_id(id)
        if not m:
            self.__log.error(f"Actualizar fallido: Mascota ID = {id} no existe")
            raise MascotaNoEncontradaError(id)
        if nombre: m.nombre = nombre
        if raza: m.raza = raza
        if peso is not None: m.peso = peso
        self.__log.info(f"Mascota actualizada: ID = {id}")
        return m

    def eliminar(self, id):
        m = self.buscar_por_id(id)
        if not m:
            self.__log.error(f"Eliminar fallido: Mascota ID = {id} no existe")
            raise MascotaNoEncontradaError(id)
        self.__bd.remove(m)
        self.__log.info(f"Mascota eliminada: ID = {id}")
        return True

    def total(self):
        return len(self.__bd)