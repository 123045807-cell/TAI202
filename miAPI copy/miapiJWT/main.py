

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
import secrets
from datetime import datetime

#app
app=FastAPI(
    title="Restaurante",
    description="API Sistema de Reservas",
    version="1.0"
)

#base de datos ficticia
reservas=[]

#Modelo validación 
class reserva(BaseModel):
    id:int = Field (..., gt=0)
    nombre_cliente:str = Field (..., min_length=6)
    fecha:datetime
    no_personas:int = Field (..., ge=1, le=10)
    estado:str = "pendiente"
    @field_validator("fecha")
    @classmethod
    def validar_fecha(cls, v):
        if v <= datetime.now():
            raise ValueError("La fecha debe ser futura")
        if v.weekday()==6:
            raise ValueError("No se permiten reservaciones en día Domingo")
        if v.hour < 8 or v.hour >=22:
            raise ValueError("Horario permitido 8:00 a 22:00")
        return v

#HTTP Basic para endponits protegidos
security = HTTPBasic()
def verificar_peticion(
    credenciales:HTTPBasicCredentials = Depends(security)
):
    usuario_ok=secrets.compare_digest(credenciales.username, "admin")
    contra_ok=secrets.compare_digest(credenciales.password, "123")

    if not (usuario_ok and contra_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Incorrectas"
        )
    return credenciales.username

#End points

#endpoint de Bienvenida
# GET
@app.get("/v1/inicio", tags=["Inicio"])
def inicio():
    return {"Mensaje":"Bienvenido al Restaurante"}
#endpoint crear reserva
#POST
@app.post("/v1/crear", tags=["Reservas"])
def crear_reserva(usuario:reserva):
    for reserva_existente in reservas:
        if reserva_existente["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="ID YA EXISTE")
    reservas.append(usuario.dict())
    return {"mensaje":"Reserva creada", "datos":usuario}
#endpoint lista reserva
#con verificacion HTTPBasic
#GET
@app.get("/v1/listar", tags=["Reservas"])
def listar_reservas(username: str = Depends(verificar_peticion)):
    return{"datos":reservas}
#endpoint consultar por ID
#GET
@app.get("/v1/consultar/{reserva_id}", tags=["Reservas"])
def consultar_reservas(reserva_id:int):
    for reservas_existente in reservas:
        if reservas_existente["id"] == reserva_id:
            return{"datos":reservas_existente}
    raise HTTPException(status_code=404, detail="No encontrado")
#endpoint confirmar reserva
#PUT
@app.put("/v1/confirmar/{id}", tags=["Reservas"])
def confirmar_reserva(id:int):
    for reserva_confirmada in reservas:
        if reserva_confirmada["id"] == id:
            reserva_confirmada["estado"]="Confirmada"
            return {"mensaje":"Confirmada", "datos":reserva_confirmada}
    raise HTTPException(status_code=404,detail="ID no encontrado")
#endpoint cancelar citas
#con verificacion HTTPBasic
#DELETE
@app.delete("/v1/eliminar/{id}")
def cancelar_cita(id:int,username:str = Depends(verificar_peticion)):
    for cancelar_cita in reservas:
        if cancelar_cita["id"] == id:
            reservas.remove(cancelar_cita)
            return {"mensaje":"Cita Cancelada", "datos":cancelar_cita}
    raise HTTPException(status_code=404, detail="Cita no encontrada")