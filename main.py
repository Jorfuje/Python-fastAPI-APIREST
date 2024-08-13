# API REST: Interfaz de Programación de Aplicaciones para compartir recursos

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las características de una API REST
app = FastAPI()

# Definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
cursos_db = []

# CRUD: Read (lectura) GET ALL: Leeremos todos los cursos de la base de datos
@app.get("/cursos/", response_model=List[Curso])
def obtenerCursos():
    return cursos_db

# CRUD: Create (escribir) POST: Agregar un nuevo curso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crearCurso(curso: Curso):
    curso.id = str(uuid.uuid4())        # Uso de UUID para generar ID único e irrepetible
    cursos_db.append(curso)

    return curso

# CRUD: Read (lectura) GET (individual): Leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtenerCurso(curso_id: str):
    cursos = (curso for curso in cursos_db if curso.id == curso_id)
    curso = next(cursos, None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


# CRUD: Update (Actualizar/Modificar) PUT: Modificar un curso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizarCurso(curso_id:str, curso_actualizado:Curso):
    cursos = (curso for curso in cursos_db if curso.id == curso_id)
    curso = next(cursos, None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso)      # Buscamos el índice exacto donde está el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    
    return curso_actualizado

# CRUD: Delete (borrado/baja) DELETE: Eliminaremos un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminarCurso(curso_id:str):
    cursos = (curso for curso in cursos_db if curso.id == curso_id)
    curso = next(cursos, None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    
    return curso
