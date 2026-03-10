#API de Sistema de Reservas de Restaurante

import secrets

from fastapi import FastAPI, status,HTTPException, Depends
from fastapi import security
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(
    title="Sistema de Reservas de Restaurante",
    description="API para reservas em um restaurante",
    version="1.0."
)

#TB fictica
reservas = []

#Modelo de validación Pydantic
class Reserva(BaseModel):
    id:int = 


#Seguridad HTTP
security = HTTPBasic

def verficar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto=secrets.compare_digest(credenciales.username,"admin")
    contrasena_correcta=secrets.compare_digest(credenciales.password,"rest123")

    if not(usuario_correcto and contrasena_correcta): 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no validas"
        )
    return credenciales.username

#endpoints

@app.post("/reserva")

@app.get("/lista")

@app.get("consulta")

@app.delete("cancelar")