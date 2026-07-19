from Config.logger import Logger

# =======================================================================================
#  SINGLETON: SistemaConfig
# =======================================================================================
class SistemaConfig:
    #guarda la unica instancia 
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "SisCita Veterinaria RX"
            cls._inst.version = "1.0"
            cls._inst.empresa = "IESTP Argentina"
            cls._inst.autor   = "Xiomara Espinoza/Ricardo Flores"
            Logger().info(
                f"Sistema Iniciado: {cls._inst.nombre} | "
                f"Version: {cls._inst.version} | "
                f"Empresa: {cls._inst.empresa} | "
                f"Autor: {cls._inst.autor}"
            )
        return cls._inst

# =======================================================================================
#  EXCEPCIONES
# =======================================================================================
class DuenoNoEncontradoError(Exception):
    def __init__(self, id): 
        super().__init__(f"Dueño ID = {id} no encontrado")


class EmailDuplicadoError(Exception):
    def __init__(self, email): 
        super().__init__(f"Email '{email}' ya registrado")
    
    
class DuenoConMascotasError(Exception):
    def __init__(self, dueno_id):
        super().__init__(f"Dueño ID = {dueno_id} no se puede eliminar: tiene mascotas asociadas")


class MascotaNoEncontradaError(Exception):
    def __init__(self, id):
        super().__init__(f"Mascota ID = {id} no encontrada")


class VeterinarioNoEncontradoError(Exception):
    def __init__(self, id):
        super().__init__(f"Veterinario ID = {id} no encontrado")


class CitaNoEncontradaError(Exception):
    def __init__(self, id): 
        super().__init__(f"Cita ID = {id} no encontrada")
    
    
class EstadoInvalidoError(Exception):
    def __init__(self, estado, validos):
        super().__init__(f"Estado inválido '{estado}'. Use uno de: {validos}")