from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, status,HTTPException, Depends

#Seguridad HTTP Basic
security = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto= secrets.compare_digest(credenciales.username,"danielaandrade")
    contrasena_correcta= secrets.compare_digest(credenciales.password,"123456")

    if not(usuario_correcto and contrasena_correcta): 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no validas"
        )
    return credenciales.username