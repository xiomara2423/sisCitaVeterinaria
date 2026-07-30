import re
from pydantic import BaseModel, field_validator
from typing import Optional

class DuenoCrear(BaseModel):
    nombre:     str
    apellido:   str
    telefono:   str
    email:      str
    direccion:  str

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        if not re.fullmatch(r"\d{9}", valor):
            raise ValueError("El teléfono debe tener 9 dígitos")
        return valor
    
    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido (ej: nombre@dominio.com)")
        return valor

class DuenoActualizar(BaseModel):
    nombre:     Optional[str] = None
    apellido:   Optional[str] = None
    telefono:   Optional[str] = None
    email:      Optional[str] = None
    direccion:  Optional[str] = None

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        if valor is not None and not re.fullmatch(r"\d{9}", valor):
            raise ValueError("El teléfono debe tener 9 dígitos")
        return valor

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        if valor is not None and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido (ej: nombre@dominio.com)")
        return valor

class DuenoRespuesta(BaseModel):
    id:         int
    nombre:     str
    apellido:   str
    telefono:   str
    email:      str
    direccion:  str