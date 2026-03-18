from fastapi import FastAPI, status,HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario 
from app.data.database import usuarios
from app.security.auth import verficar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

######################################################
@router.get("/")
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status":"200"
    }
@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario:crear_usuario):#usamos el modelo
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuarios Creado",
        "Usuario":usuario
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