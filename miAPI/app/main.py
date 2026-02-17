# importaciones
from operator import index
from fastapi import FastAPI, status,HTTPException
from typing import Optional
import asyncio

app = FastAPI(
    title= "Mi primer API",
    description= "Daniela Andrade Botello",
    version="1.0"
)

#TB FICTICIA
usuarios=[
    {"id":1,"nombre":"Fany","edad":21},
    {"id":2,"nombre":"Dani","edad":22},
    {"id":3,"nombre":"Sofi","edad":20}
]

#endpoints
@app.get("/")
async def holamunddi():
    return{"mensaje":"Hola mundo FastAP"}
        
@app.get("/bienbenido")
async def bienbenido():
    await asyncio
    return{
        "mensaje":"Bienvenido a FATAPI",
        "estatus":"200",
        }
    
@app.get("/v1/parametro0b/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/parametro0b/{id}",tags=['Parametro Opcional'])
async def consulta_dos(id:Optional[int]=None):
    if id is not None:
        return {"mensaje":"usuario encontrado",
                "usuario":id,
                "status":"200"
                }
    else:
        return {"mensaje":"No se proporcionó un ID",
                "status":"400"
                }

            ######################################################
@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }
@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mmensaje":"Usuarios Creado",
        "Datos nuevos": usuario
    }
@app.put("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuario_actualizado["id"] = usuario_id
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado",
                "datos_anteriores": usr,
                "datos_nuevos": usuario_actualizado
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )


@app.patch("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(usuario_id: int, campos: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios[index].update(campos)
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "datos_actualizados": usuarios[index]
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )


@app.delete("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado",
                "datos_eliminados": usr
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )