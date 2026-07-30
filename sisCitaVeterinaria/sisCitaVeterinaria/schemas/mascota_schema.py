import re
from pydantic import BaseModel, field_validator
from typing import Optional

class MascotaCrear(BaseModel):
    dueno_id: int
    nombre:   str
    especie:  str
    raza:     Optional[str] = None
    sexo:     Optional[str] = None
    peso:     Optional[float] = None

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, valor):
        if valor is not None and valor not in ("M", "H"):
            raise ValueError("El sexo debe ser 'M' (Macho) o 'H' (Hembra)")
        return valor

    @field_validator("peso")
    @classmethod
    def validar_peso(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        return valor

class MascotaActualizar(BaseModel):
    dueno_id: Optional[int] = None
    nombre:   Optional[str] = None
    especie:  Optional[str] = None
    raza:     Optional[str] = None
    sexo:     Optional[str] = None
    peso:     Optional[float] = None

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, valor):
        if valor is not None and valor not in ("M", "H"):
            raise ValueError("El sexo debe ser 'M' (Macho) o 'H' (Hembra)")
        return valor

    @field_validator("peso")
    @classmethod
    def validar_peso(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("El peso debe ser un número positivo mayor a 0")
        return valor

class MascotaRespuesta(BaseModel):
    id:       int
    dueno_id: int
    nombre:   str
    especie:  str
    raza:     Optional[str] = None
    sexo:     Optional[str] = None
    peso:     Optional[float] = None
