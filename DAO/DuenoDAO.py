from Config.logger import Logger

class DuenoNoEncontradoError(Exception):
    def __init__(self, id): super().__init__(f"Dueño ID = {id} no encontrado")

class EmailDuplicadoError(Exception):
    def __init__(self, email): super().__init__(f"Email '{email}' ya registrado")

class DuenoDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_email(self, email):
        for d in self.__bd:
            if d.email == email:
                return d
        return None

    def buscar_por_id(self, id):
        for d in self.__bd:
            if d.id == id:
                return d
        return None

    def insertar(self, dueno):
        if dueno.email and self.buscar_por_email(dueno.email):
            self.__log.warning(f"Email duplicado: {dueno.email}")
            raise EmailDuplicadoError(dueno.email)
        dueno.id = self.__cid
        self.__cid += 1
        self.__bd.append(dueno)
        self.__log.info(f"Dueño agregado: {dueno.nombre} {dueno.apellido} (ID = {dueno.id})")
        return dueno

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda d: d.nombre)

    def actualizar(self, id, nombre=None, telefono=None, email=None, direccion=None):
        d = self.buscar_por_id(id)
        if not d:
            self.__log.error(f"Actualizar fallido: Dueño ID = {id} no existe")
            raise DuenoNoEncontradoError(id)
        email = email.strip().lower() if email else None
        if email and email != d.email and self.buscar_por_email(email):
            raise EmailDuplicadoError(email)
        if nombre: d.nombre = nombre
        if telefono: d.telefono = telefono
        if email: d.email = email
        if direccion: d.direccion = direccion
        self.__log.info(f"Dueño actualizado: ID = {id}")
        return d

    def eliminar(self, id):
        d = self.buscar_por_id(id)
        if not d:
            self.__log.error(f"Eliminar fallido: Dueño ID = {id} no existe")
            raise DuenoNoEncontradoError(id)
        self.__bd.remove(d)
        self.__log.info(f"Dueño eliminado: ID = {id}")
        return True

    def total(self):
        return len(self.__bd)