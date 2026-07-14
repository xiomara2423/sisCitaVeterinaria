class Veterinario:
    def __init__(self, nombre, apellido, especialidad, telefono, disponible=True):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.telefono = telefono
        self.disponible = disponible

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.id}] {self.nombre} {self.apellido} | {self.especialidad} | {estado}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "especialidad": self.especialidad,
            "telefono": self.telefono,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, datos):
        v = cls(datos["nombre"], datos["apellido"], datos["especialidad"], datos["telefono"], datos["disponible"])
        v.id = datos["id"]
        return v