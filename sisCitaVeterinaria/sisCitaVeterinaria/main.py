from Config.logger import Logger
from Config.sistema_config import SistemaConfig
from DAO.DuenoDAO import DuenoDAO
from DAO.MascotaDAO import MascotaDAO
from DAO.VeterinarioDAO import VeterinarioDAO
from DAO.CitaDAO import CitaDAO

 
from Vistas.menu import (
                        cargar_datos_ejemplo,
                        mostrar_menu,
                        agregar_dueno, listar_duenos, actualizar_dueno, eliminar_dueno,
                        agregar_mascota, listar_mascotas, actualizar_mascota, eliminar_mascota,
                        agregar_veterinario, listar_veterinarios, actualizar_veterinario, eliminar_veterinario,
                        agendar_cita, listar_citas, eliminar_cita, actualizar_cita,
                        ver_duenos_json, ver_mascotas_json, ver_veterinarios_json, ver_citas_json)
 
def main():
    cfg = SistemaConfig()
    dueno_dao = DuenoDAO()
    mascota_dao = MascotaDAO()
    vet_dao = VeterinarioDAO()
    cita_dao = CitaDAO()
 
    #=======================
    #UBICADO EN PERSISTENCIA
    #=======================
    cargar_duenos(dueno_dao)
    cargar_mascotas(mascota_dao)
    cargar_veterinarios(vet_dao)
    cargar_citas(cita_dao)
 
    # Si no había JSON previo (primera ejecución), arranca con datos de ejemplo
    if dueno_dao.total() == 0 and vet_dao.total() == 0:
        cargar_datos_ejemplo(dueno_dao, mascota_dao, vet_dao, cita_dao)
 
    while True:
        mostrar_menu(cfg)
        opcion = input("  Elige una opción: ").strip()
        match opcion:
            case "1": agregar_dueno(dueno_dao)
            case "2": agregar_mascota(mascota_dao, dueno_dao)
            case "3": agregar_veterinario(vet_dao)
            case "4": agendar_cita(cita_dao, mascota_dao, vet_dao)
            case "5": listar_duenos(dueno_dao)
            case "6": listar_mascotas(mascota_dao)
            case "7": listar_veterinarios(vet_dao)
            case "8": listar_citas(cita_dao)
            case "9": actualizar_dueno(dueno_dao)
            case "10": actualizar_mascota(mascota_dao)
            case "11": actualizar_veterinario(vet_dao)
            case "12": actualizar_cita(cita_dao)
            case "13": eliminar_dueno(dueno_dao)
            case "14": eliminar_mascota(mascota_dao)
            case "15": eliminar_veterinario(vet_dao)
            case "16": eliminar_cita(cita_dao)
            #==========================
            #FUNCIONALIDADES EN MENU.PY
            #==========================
            case "17": ver_duenos_json(dueno_dao)
            case "18": ver_mascotas_json(mascota_dao)
            case "19": ver_veterinarios_json(vet_dao)
            case "20": ver_citas_json(cita_dao)
           
            #=========================================================
            case "21": Logger().mostrar_logs()
            case "22": Logger().limpiar()
            case "0":
                
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego")
                break
            case _:
                print("  Opción no válida, elija entre 0 y 23")
 
if __name__ == "__main__":
    main()