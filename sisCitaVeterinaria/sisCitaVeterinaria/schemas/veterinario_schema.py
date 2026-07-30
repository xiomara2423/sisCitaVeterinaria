import re
from pydantic import BaseModel, field_validator
from typing import Optional

class VeterinarioCrear(BaseModel):
    nombre:       str
    apellido:     str
    especialidad: str
    telefono:     str
    disponible:   bool = True

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        # Valida número de teléfono
        if not re.fullmatch(r"\d{9}", valor):
            raise ValueError("El teléfono debe tener 9 dígitos")
        return valor

class VeterinarioActualizar(BaseModel):
    nombre:       Optional[str] = None
    apellido:     Optional[str] = None
    especialidad: Optional[str] = None
    telefono:     Optional[str] = None
    disponible:   Optional[bool] = None

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        if valor is not None and not re.fullmatch(r"\d{9}", valor):
            raise ValueError("El teléfono debe tener 9 dígitos")
        return valor

class VeterinarioRespuesta(BaseModel):
    id:           int
    nombre:       str
    apellido:     str
    especialidad: str
    telefono:     str
    disponible:   bool