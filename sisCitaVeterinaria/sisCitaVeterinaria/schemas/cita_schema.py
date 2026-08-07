from pydantic import BaseModel, field_validator
from typing import Optional
from Modelos.Cita import Cita 

class CitaCrear(BaseModel):
    mascota_id:     int
    veterinario_id: int
    fecha:          str
    motivo:         str
    estado:         str = "Programada"

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor):
        if valor not in Cita.E_Validos:
            raise ValueError(f"Estado inválido '{valor}'. Use uno de: {Cita.E_Validos}")
        return valor

class CitaActualizar(BaseModel):
    estado: Optional[str] = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor):
        if valor is not None and valor not in Cita.E_Validos:
            raise ValueError(f"Estado inválido '{valor}'. Use uno de: {Cita.E_Validos}")
        return valor

class CitaRespuesta(BaseModel):
    id: int
    mascota_id: int
    veterinario_id: int
    fecha: str
    motivo: str
    estado: str