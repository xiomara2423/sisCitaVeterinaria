from fastapi import APIRouter
from Config.logger import Logger
from Config.sistema_config import SistemaConfig

router = APIRouter(prefix="/sistema", tags=["Sistema"])

@router.get("/config")
def obtener_config():
    cfg = SistemaConfig()
    return {"nombre": cfg.nombre, "version": cfg.version, "empresa": cfg.empresa, "autor": cfg.autor}

@router.get("/logs")
def listar_logs():
    return Logger().obtener_logs()

@router.delete("/logs")
def limpiar_logs():
    Logger().limpiar()
    return {"mensaje": "Logs limpiados"}