#API de Sistema de Reservas de Restaurante: crear reserva, lista reserva, consultar por ID, confirmar reserva.
#Modelo datos obligatorios: nombre cliente min 6 caracteres, fecha reserva futura entre 8:00am y 10:00pm, no en domingo.
#Protegidas: listas reservas y cancelar citas con verificar_peticion

import secrets

from fastapi import FastAPI, status,HTTPException, Depends
from fastapi import security
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime

app = FastAPI(
    title="Sistema de Reservas de Restaurante",
    description="API para reservas em um restaurante",
    version="1.0."
)

#TB fictica
reservas = []

#Modelo de validación Pydantic
class reserva(BaseModel):
    id: int =Field(..., gt=0, description="Identificador de reserva")
    nombre_cliente: str = Field(..., min_length=6)
    fecha_reserva: str = Field(..., description="Fecha de reserva en formato YYYY-MM-DD HH:MM", )
    no_personas: int = Field(..., ge=1, le=10, description="Número de personas permitidas entre 1 y 10")


#Seguridad HTTP
security = HTTPBasic

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto=secrets.compare_digest(credenciales.username,"admin")
    contrasena_correcta=secrets.compare_digest(credenciales.password,"rest123")

    if not(usuario_correcto and contrasena_correcta): 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no validas"
        )
    return credenciales.username

#endpoints 
@app.post("/v1/reserva/", tags=['HTTP CRUD'] ,status_code=status.HTTP_201_CREATED)
async def crear_reserva(usuario:reserva)
    for usr in reservas:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    reservas.append(usuario)
    return{
        "mensaje":"Reserva Creada",
        "Reserva":usuario
    }


@app.get("/v1/reserva")

@app.get("/v1/reserva/{reserva_id}")
async def obtener_reserva(reserva_id: int):
    for usr in reservas:
        if usr["id"] == reserva_id:
            return usr
    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrada"
    )

@app.patch("/v1/reserva/{reserva_id}", tags=['HTTP CRUD'])
async def actualizar_reserva_parcial (reserva_id:int, campos: dict, usuarioAuth:str = Depends(verificar_peticion)):
    for index, usr in enumerate(reservas):
        if usr["id"] == reserva_id:
         reservas[index].update(campos)
         return {
             "mensaje":"Reserva actualizada",
             "datos_adctualizados" : reservas[index]
         }
        
        raise HTTPException(
            status_code=404
            detail = "El id no existe"
        )
       
    