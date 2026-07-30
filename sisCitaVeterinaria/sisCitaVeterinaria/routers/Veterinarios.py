from fastapi import APIRouter, HTTPException
from DAO.VeterinarioDAO import VeterinarioDAO, VeterinarioNoEncontradoError, VeterinarioConCitasError
from Modelos.Veterinario import Veterinario
from schemas.veterinario_schema import VeterinarioCrear, VeterinarioActualizar, VeterinarioRespuesta

router = APIRouter(prefix="/veterinarios", tags=["Veterinarios"])
dao = VeterinarioDAO()

@router.get("/", response_model=list[VeterinarioRespuesta])
def listar_veterinarios():
    return [d.to_dict() for d in dao.obtener_todos()]

@router.get("/{veterinario_id}", response_model=VeterinarioRespuesta)
def obtener_veterinario(veterinario_id: int):
    d = dao.buscar_por_id(veterinario_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"Veterinario ID = {veterinario_id} no encontrado")
    return d.to_dict()

@router.post("/", response_model=VeterinarioRespuesta, status_code=201)
def crear_veterinario(datos: VeterinarioCrear):
    d = dao.insertar(Veterinario(datos.nombre, datos.apellido, datos.especialidad, datos.telefono, datos.disponible))
    return d.to_dict()

@router.put("/{veterinario_id}", response_model=VeterinarioRespuesta)
def actualizar_veterinario(veterinario_id: int, datos: VeterinarioActualizar):
    try:
        d = dao.actualizar(veterinario_id, datos.nombre, datos.apellido, datos.especialidad, datos.telefono, datos.disponible)
        return d.to_dict()
    except VeterinarioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex)) 

@router.delete("/{veterinario_id}")
def eliminar_veterinario(veterinario_id: int):
    try:
        dao.eliminar(veterinario_id)
        return {"mensaje": f"Veterinario ID = {veterinario_id} eliminado"}
    except VeterinarioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except VeterinarioConCitasError as ex:
        raise HTTPException(status_code=409, detail=str(ex))