from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.models import LibroCreate, LibroResponse, PrestamoCreate, PrestamoResponse

app = FastAPI(
    title="Biblioteca Digital API",
    description="API para el control de una Biblioteca Digital",
    version="1.0"
)

#Base de datos simulada
libros={}
libro_counter=1
prestamos={}
prestamo_counter=1

@app.get("/bienvenido")
async def bienvenido():
    return {
        "mensaje": "Bienvenido a la API de Biblioteca Digital",
        "estatus": "200"
    }

@app.post("/libros", response_model=LibroResponse, status_code=201)
async def registrar_libro(libro: LibroCreate):
    global libro_counter

    for libro_existente in libros.values():
        if libro_existente["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="Ya existe un libro con ese nombre")

    nuevo_libro = {
        "id": libro_counter,
        "nombre": libro.nombre,
        "autor": libro.autor,
        "year": libro.year,
        "paginas": libro.paginas,
        "estado": "disponible"
    }

    libros[libro_counter] = nuevo_libro
    libro_counter += 1
    return nuevo_libro

@app.get("/libros", response_model=list[LibroResponse])
async def listar_libros():
    return list(libros.values())

@app.get("/libros/buscar", response_model=LibroResponse)
async def buscar_libro(nombre: str):
    for libro_existente in libros.values():
        if libro_existente["nombre"].lower() == nombre.lower():
            return libro_existente
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/prestamos", response_model=PrestamoResponse, status_code=201)
async def registrar_prestamo(prestamo: PrestamoCreate):
    global prestamo_counter

    if prestamo.libro_id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    if libros[prestamo.libro_id]["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    nuevo_prestamo = {
        "id": prestamo_counter,
        "libro_id": prestamo.libro_id,
        "usuario": prestamo.usuario,
        "fecha_prestamo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "devuelto": False
    }

    prestamos[prestamo_counter] = nuevo_prestamo
    libros["estado"] = "prestado"
    prestamo_counter += 1
    return nuevo_prestamo

@app.put("/prestamos/{prestamo_id}/devolver")
async def devolver_libro(prestamo_id: int):
    if prestamo_id not in prestamos:
        raise HTTPException(status_code=409, detail="El registro de préstamo no existe")

    if prestamos[prestamo_id]["devuelto"]:
        raise HTTPException(status_code=409, detail="El libro ya fue devuelto anteriormente")

    prestamos[prestamo_id]["devuelto"] = True
    libros[prestamos[prestamo_id]["libro_id"]]["estado"] = "disponible"
    return {"mensaje": "Libro devuelto correctamente", "estatus": "200"}

@app.delete("/prestamos/{prestamo_id}")
async def eliminar_prestamo(prestamo_id: int):
    if prestamo_id not in prestamos:
        raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")

    prestamo = prestamos.pop(prestamo_id)

    if not prestamo["devuelto"]:
        libros[prestamo["libro_id"]]["estado"] = "disponible"

    return {"mensaje": f"Préstamo {prestamo_id} eliminado correctamente", "estatus": "200"}