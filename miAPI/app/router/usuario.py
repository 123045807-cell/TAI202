from fastapi import FastAPI, status,HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario 
from app.security.auth import verficar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuarios import Usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

######################################################
@router.get("/")
async def leer_usuarios(db:Session = Depends(get_db)):
    queryUsuarios= db.query(dbUsuario).all()
    return{
        "total":len(queryUsuarios),
        "usuarios":queryUsuarios,
        "status":"200"
    }
@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP:crear_usuario, db:Session= Depends(get_db)):#usamos el modelo
    nuevoU= dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return{
        "mensaje":"Usuarios Agregado",
        "Usuario":usuarioP
    }
@router.put("/{usuario_id}", status_code=status.HTTP_200_OK)
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


@router.patch("/{usuario_id}",status_code=status.HTTP_200_OK)
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


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(usuario_id: int, usuarioAuth:str = Depends(verficar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "datos_eliminados": usr
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )