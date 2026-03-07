#Importaciones
from fastapi import FastAPI, status,HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from datetime import datetime, timedelta


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

#Modelo de Validacion pydantic
class crear_usuario(BaseModel):
    id:int=Field(...,gt=0, description="Identificador de usuario")
    nombre:str=Field(..., min_length=3, max_length=50, examples=["Juanita"])
    edad:int=Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

#Modelo pydantic para usuario de autenticacion
class usuario_login(BaseModel):
    username:str
    password:str

#TB FICTICIA de usuarios
usuarios_auth=[
    usuario_login(username="danielaandrade", password="123456")
]

#Configuracion JWT
SECRET_KEY="clave-super-secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

#Seguridad OAuth2
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def crear_token(data:dict):
    payload=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp":expire})
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def verificar_token(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado"
        )
    return username

#endpoint de login
@app.post("/token",tags=['Autenticacion'])
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
    usuario=next((u for u in usuarios_auth if u.username==form_data.username and u.password==form_data.password),None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )
    token=crear_token(data={"sub":usuario.username})
    return{"access_token":token,"token_type":"bearer"}

#endpoints
@app.get("/")
async def holamundo():
    return{"mensaje":"Hola mundo FastAP"}
        
@app.get("/bienvenido")
async def bienvenido():
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
@app.post("/v1/usuarios/", tags=['HTTP CRUD'] ,status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario:crear_usuario):#usamos el modelo
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.model_dump())
    return{
        "mensaje":"Usuarios Creado",
        "Usuario":usuario
    }
@app.put("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario_actualizado: dict, usuarioAuth:str=Depends(verificar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuario_actualizado["id"] = usuario_id
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": f"Usuario actualizado por {usuarioAuth}",
                "datos_anteriores": usr,
                "datos_nuevos": usuario_actualizado
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )


@app.patch("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(usuario_id: int, campos: dict, usuarioAuth:str=Depends(verificar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios[index].update(campos)
            return {
                "mensaje": f"Usuario actualizado parcialmente por {usuarioAuth}",
                "datos_actualizados": usuarios[index]
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )


@app.delete("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int, usuarioAuth:str=Depends(verificar_token)):
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