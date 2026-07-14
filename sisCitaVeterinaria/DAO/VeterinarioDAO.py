from Config.logger import Logger

class VeterinarioNoEncontradoError(Exception):
    def __init__(self, id): super().__init__(f"Veterinario ID = {id} no encontrado")

class VeterinarioDAO:
    def __init__(self):
        self.__bd = []
        self.__vid = 1
        self.__log = Logger()

    def buscar_por_id(self, id):
        for v in self.__bd:
            if v.id == id:
                return v
        return None

    def insertar(self, veterinario):
        veterinario.id = self.__vid
        self.__vid += 1
        self.__bd.append(veterinario)
        self.__log.info(f"Veterinario agregado: {veterinario.nombre} {veterinario.apellido} (ID = {veterinario.id})")
        return veterinario

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda v: v.nombre)

    def actualizar(self, id, especialidad=None, telefono=None, disponible=None):
        v = self.buscar_por_id(id)
        if not v:
            self.__log.error(f"Actualizar fallido: Veterinario ID = {id} no existe")
            raise VeterinarioNoEncontradoError(id)
        if especialidad: v.especialidad = especialidad
        if telefono: v.telefono = telefono
        if disponible is not None: v.disponible = disponible
        self.__log.info(f"Veterinario actualizado: ID = {id}")
        return v

    def eliminar(self, id):
        v = self.buscar_por_id(id)
        if not v:
            self.__log.error(f"Eliminar fallido: Veterinario ID = {id} no existe")
            raise VeterinarioNoEncontradoError(id)
        self.__bd.remove(v)
        self.__log.info(f"Veterinario eliminado: ID = {id}")
        return True

    def total(self):
        return len(self.__bd)
