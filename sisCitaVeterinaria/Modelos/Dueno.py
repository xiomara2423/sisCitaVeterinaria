class Dueno:
    def __init__(self, nombre, apellido, telefono, email, direccion):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email.strip().lower() if email else None
        self.direccion = direccion

    def __str__(self):
        return f"[{self.id}] {self.nombre} {self.apellido} | Tel: {self.telefono} | {self.email} | {self.direccion}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion
        }

    @classmethod
    def from_dict(cls, datos):
        d = cls(datos["nombre"], datos["apellido"], datos["telefono"], datos["email"], datos["direccion"])
        d.id = datos["id"]
        return d