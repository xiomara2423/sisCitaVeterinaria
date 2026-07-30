from fastapi import APIRouter, HTTPException
from DAO.CitaDAO import CitaDAO, CitaNoEncontradaError, EstadoInvalidoError
from Modelos.Cita import Cita
from schemas.cita_schema import CitaCrear, CitaActualizar, CitaRespuesta

router = APIRouter(prefix="/citas", tags=["Citas"])
dao = CitaDAO()

@router.get("/", response_model=list[CitaRespuesta])
def listar_citas():
    return [c.to_dict() for c in dao.obtener_todos()]

@router.get("/{cita_id}", response_model=CitaRespuesta)
def obtener_cita(cita_id: int):
    c = dao.buscar_por_id(cita_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cita ID = {cita_id} no encontrada")
    return c.to_dict()

@router.post("/", response_model=CitaRespuesta, status_code=201)
def crear_cita(datos: CitaCrear):
    try:
        c = dao.insertar(Cita(datos.mascota_id, datos.veterinario_id, datos.fecha, datos.motivo))
        return c.to_dict()
    except EstadoInvalidoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{cita_id}", response_model=CitaRespuesta)
def actualizar_cita(cita_id: int, datos: CitaActualizar):
    try:
        c = dao.actualizar(cita_id, datos.motivo, datos.estado)
        return c.to_dict()
    except CitaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except EstadoInvalidoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int):
    try:
        dao.eliminar(cita_id)
        return {"mensaje": f"Cita ID = {cita_id} eliminada"}
    except CitaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))