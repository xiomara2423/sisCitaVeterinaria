from fastapi import APIRouter, HTTPException
from DAO.MascotaDAO import MascotaDAO, MascotaNoEncontradaError, MascotaConCitasError
from Modelos.Mascota import Mascota
from schemas.mascota_schema import MascotaCrear, MascotaActualizar, MascotaRespuesta

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])
dao = MascotaDAO()

@router.get("/", response_model=list[MascotaRespuesta])
def listar_mascotas():
    return [m.to_dict() for m in dao.obtener_todos()]

@router.get("/{mascota_id}", response_model=MascotaRespuesta)
def obtener_mascota(mascota_id: int):
    m = dao.buscar_por_id(mascota_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Mascota ID = {mascota_id} no encontrada")
    return m.to_dict()

@router.post("/", response_model=MascotaRespuesta, status_code=201)
def crear_mascota(datos: MascotaCrear):
    m = dao.insertar(Mascota(datos.dueno_id, datos.nombre, datos.especie, datos.raza, datos.sexo, datos.peso))
    return m.to_dict()

@router.put("/{mascota_id}", response_model=MascotaRespuesta)
def actualizar_mascota(mascota_id: int, datos: MascotaActualizar):
    try:
        m = dao.actualizar(mascota_id, datos.nombre, datos.raza, datos.peso)
        return m.to_dict()
    except MascotaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{mascota_id}")
def eliminar_mascota(mascota_id: int):
    try:
        dao.eliminar(mascota_id)
        return {"mensaje": f"Mascota ID = {mascota_id} eliminada"}
    except MascotaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except MascotaConCitasError as ex:
        raise HTTPException(status_code=409, detail=str(ex))