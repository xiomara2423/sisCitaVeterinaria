from fastapi import APIRouter, HTTPException
from DAO.DuenoDAO import DuenoDAO, DuenoNoEncontradoError, DuenoConMascotasError, EmailDuplicadoError
from Modelos.Dueno import Dueno
from schemas.dueno_schema import DuenoCrear, DuenoActualizar, DuenoRespuesta

router = APIRouter(prefix="/duenos", tags=["Dueños"])
dao = DuenoDAO()

@router.get("/", response_model=list[DuenoRespuesta])
def listar_duenos():
    return [d.to_dict() for d in dao.obtener_todos()]

@router.get("/{dueno_id}", response_model=DuenoRespuesta)
def obtener_dueno(dueno_id: int):
    d = dao.buscar_por_id(dueno_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"Dueno ID = {dueno_id} no encontrado")
    return d.to_dict()

@router.post("/", response_model=DuenoRespuesta, status_code=201)
def crear_dueno(datos: DuenoCrear):
    try:
        d = dao.insertar(Dueno(datos.nombre, datos.apellido, datos.telefono, datos.email, datos.direccion))
        return d.to_dict()
    except EmailDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{dueno_id}", response_model=DuenoRespuesta)
def actualizar_dueno(dueno_id: int, datos: DuenoActualizar):
    try:
        d = dao.actualizar(dueno_id, datos.nombre, datos.apellido, datos.telefono, datos.email, datos.direccion)
        return d.to_dict()
    except DuenoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except EmailDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))    

@router.delete("/{dueno_id}")
def eliminar_dueno(dueno_id: int):
    try:
        dao.eliminar(dueno_id)
        return {"mensaje": f"Dueno ID = {dueno_id} eliminado"}
    except DuenoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except DuenoConMascotasError as ex:
        raise HTTPException(status_code=409, detail=str(ex))