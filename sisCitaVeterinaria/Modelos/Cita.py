class Cita:
    E_Validos = ("Programada", "Completada", "Cancelada")

    def __init__(self, mascota_id, veterinario_id, fecha, motivo, estado="Programada"):
        self.id = None
        self.mascota_id = mascota_id
        self.veterinario_id = veterinario_id
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado

    def __str__(self):
        return f"[{self.id}] {self.fecha} | Mascota: {self.mascota_id} Vet: {self.veterinario_id} | {self.motivo} | {self.estado}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "mascota_id": self.mascota_id,
            "veterinario_id": self.veterinario_id,
            "fecha": self.fecha,
            "motivo": self.motivo,
            "estado": self.estado
        }

    @classmethod
    def from_dict(cls, datos):
        c = cls(datos["mascota_id"], datos["veterinario_id"], datos["fecha"], datos["motivo"], datos["estado"])
        c.id = datos["id"]
        return c