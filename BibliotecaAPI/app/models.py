from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from datetime import datetime

CURRENT_YEAR = datetime.now().year

class LibroCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=250)
    autor: str = Field(..., min_length=2, max_length=250)
    year: int
    paginas: int

    @field_validator("year")
    @classmethod
    def validar_year(cls, v):
        if v <= 1450 or v > CURRENT_YEAR:
            raise ValueError(f"El año debe ser mayor a 1450 y menor o igual a {CURRENT_YEAR}")
        return v

    @field_validator("paginas")
    @classmethod
    def validar_paginas(cls, v):
        if v < 1:
            raise ValueError("Las páginas deben ser un entero positivo mayor a 1")
        return v

class LibroResponse(LibroCreate):
    id: int
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=250)
    correo: EmailStr

class PrestamoCreate(BaseModel):
    libro_id: int
    usuario: Usuario

class PrestamoResponse(BaseModel):
    id: int
    libro_id: int
    usuario: Usuario
    fecha_prestamo: str
    devuelto: bool = False