import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

misc =APIRouter(tags=["Varios"])


#endpoints
@misc.get("/")
async def holamundo():
    return{"mensaje":"Hola mundo FastAP"}
        
@misc.get("/bienvenido")
async def bienvenido():
    await asyncio
    return{
        "mensaje":"Bienvenido a FATAPI",
        "estatus":"200",
        }
    
@misc.get("/v1/parametro0b/{id}")
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200"
            }

@misc.get("/v1/parametro0b/{id}")
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

           