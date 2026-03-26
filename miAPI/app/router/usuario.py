from fastapi import FastAPI, status,HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario 
from app.models.usuario import actualizar_usuario
from app.models.usuario import actualizar_usuario_parcial
from app.security.auth import verificar_peticion


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

@router.get("/{usuario_id}",status_code=status.HTTP_200_OK)
async def leer_usuario(usuario_id:int, db:Session = Depends(get_db)):
    usuarioQ= db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not usuarioQ:
        raise HTTPException(
                status_code=404,
                detail="El id no existe"
        )
    return{
        "Usuario":usuarioQ
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP:crear_usuario, db:Session= Depends(get_db)):#usamos el modelo
    nuevoU= dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return{
        "mensaje":"Usuarios Agregado",
        "Usuario":nuevoU
    }
@router.put("/{usuario_id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(usuario_id:int,usuarioP:actualizar_usuario, db:Session = Depends(get_db)):
    usuarioQ= db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first() 
    if not usuarioQ:
        raise HTTPException(
                status_code=404,
                detail="El id no existe"
        )
    usuarioQ.nombre= usuarioP.nombre
    usuarioQ.edad= usuarioP.edad
    db.commit()
    db.refresh(usuarioQ)
    return {
        "mensaje": "Usuario actualizado",
        "Usuario": usuarioQ
    }

@router.patch("/{usuario_id}",status_code=status.HTTP_200_OK)
async def patch_usuario(usuario_id: int, campos: actualizar_usuario_parcial, db:Session = Depends(get_db)):
    usuarioQ= db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not usuarioQ:
        raise HTTPException(
                status_code=404,
                detail="El id no existe"
        )
    for key, value in campos.model_dump(exclude_unset=True).items():
        if hasattr(usuarioQ, key):
            setattr(usuarioQ, key, value)
    db.commit()
    db.refresh(usuarioQ)
    return {
        "mensaje": "Usuario actualizado parcialmente",
        "Usuario": usuarioQ
    }

@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(usuario_id:int, db:Session = Depends(get_db), usuarioAuth:str = Depends(verificar_peticion)):
    usuarioQ= db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()

    if not usuarioQ:
        raise HTTPException(status_code=404, detail="El id no existe")
    
    nombre_eliminado = usuarioQ.nombre
    db.delete(usuarioQ)
    db.commit()
    return{
        "mensaje":f"Usuario eliminado por {usuarioAuth}",
        "usuario_eliminado" : nombre_eliminado
    }