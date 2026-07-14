class Mascota:
    def __init__(self, dueno_id, nombre, especie, raza, sexo, peso):
        self.id = None
        self.dueno_id = dueno_id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.peso = peso

    def __str__(self):
        return f"[{self.id}] {self.nombre} ({self.especie}, {self.raza}) | Sexo:{self.sexo} | {self.peso}kg"
    
    def to_dict(self):
        return {
            "id": self.id,
            "dueno_id": self.dueno_id,
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "sexo": self.sexo,
            "peso": self.peso
        }

    @classmethod
    def from_dict(cls, datos):
        m = cls(datos["dueno_id"], datos["nombre"], datos["especie"], datos["raza"], datos["sexo"], datos["peso"])
        m.id = datos["id"]
        return m