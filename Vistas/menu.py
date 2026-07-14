import json

from Modelos.Dueno import Dueno
from Modelos.Mascota import Mascota
from Modelos.Veterinario import Veterinario
from Modelos.Cita import Cita
from DAO.DuenoDAO import DuenoNoEncontradoError, EmailDuplicadoError
from DAO.MascotaDAO import MascotaNoEncontradaError
from DAO.VeterinarioDAO import VeterinarioNoEncontradoError
from DAO.CitaDAO import CitaNoEncontradaError, EstadoInvalidoError


def cargar_datos_ejemplo(dueno_dao, mascota_dao, vet_dao, cita_dao):
    d1 = dueno_dao.insertar(Dueno("Juan", "Perez", "987654321", "juanperez@gmail.com", "av las paltas 505"))
    d2 = dueno_dao.insertar(Dueno("Maria", "Nuñez", "987654322", "marianunez@gmail.com", "av las peras 556"))

    m1 = mascota_dao.insertar(Mascota(d1.id, "Poli", "Perro", "Mestizo", "H", 15))
    m2 = mascota_dao.insertar(Mascota(d2.id, "Roco", "Gato", "Mestizo", "M", 8))

    v1 = vet_dao.insertar(Veterinario("Anthonio", "Vasquez", "Oftalmologo", "987654334"))
    v2 = vet_dao.insertar(Veterinario("Laura", "Roca", "Cirujana", "983654334"))

    cita_dao.insertar(Cita(m1.id, v1.id, "01-04-2026 08:30:00", "Chequeo visual"))
    cita_dao.insertar(Cita(m2.id, v2.id, "01-06-2026 10:00:00", "Cirugia gastrica"))

# =======================================================================================
#  MENÚ / INTERFAZ DE CONSOLA
# =======================================================================================
def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f"  {cfg.nombre} v{cfg.version}")
    print(f"  {cfg.empresa}")
    print(f"  {cfg.autor}")
    print(f"{'=' * 45}")
    print(" 1.  Agregar dueño")
    print(" 2.  Agregar mascota")
    print(" 3.  Agregar veterinario")
    print(" 4.  Agendar cita")
    print(" 5.  Listar dueños")
    print(" 6.  Listar mascotas")
    print(" 7.  Listar veterinarios")
    print(" 8.  Listar citas")
    print(" 9.  Actualizar dueño")
    print(" 10. Actualizar mascota")
    print(" 11. Actualizar veterinario")
    print(" 12. Cambiar estado de cita")
    print(" 13. Eliminar dueño")
    print(" 14. Eliminar mascota")
    print(" 15. Eliminar veterinario")
    print(" 16. Eliminar cita")
    print(" 17. Ver dueños en JSON")
    print(" 18. Ver mascotas en JSON")
    print(" 19. Ver veterinarios en JSON")
    print(" 20. Ver citas en JSON")
    print(" 21. Guardar datos en JSON")
    print(" 22. Ver historial de logs")
    print(" 23. Limpiar historial de logs")
    print(" 0.  Salir")
    print(f"{'=' * 45}")

def agregar_dueno(dao):
    print("\n--- AGREGAR DUEÑO ---")
    nombre    = input(" Nombre    : ")
    apellido  = input(" Apellido  : ")
    telefono  = input(" Teléfono  : ")
    email     = input(" Email     : ").strip() or None
    direccion = input(" Dirección : ")
    try:
        d = dao.insertar(Dueno(nombre, apellido, telefono, email, direccion))
        print(f" OK Dueño agregado con ID = {d.id}")
    except EmailDuplicadoError as ex:
        print(f" ERROR: {ex}")

def agregar_mascota(dao_m, dao_d):
    print("\n--- AGREGAR MASCOTA ---")
    try:
        dueno_id = int(input(" ID del dueño : "))
        if not dao_d.buscar_por_id(dueno_id):
            raise DuenoNoEncontradoError(dueno_id)
        nombre  = input(" Nombre  : ")
        especie = input(" Especie : ")
        raza    = input(" Raza    : ")
        sexo    = input(" Sexo (M/H): ").upper()
        peso    = float(input(" Peso    : "))
        m = dao_m.insertar(Mascota(dueno_id, nombre, especie, raza, sexo, peso))
        print(f" OK Mascota agregada con ID = {m.id}")
    except DuenoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser entero y el peso un número")

def agregar_veterinario(dao):
    print("\n--- AGREGAR VETERINARIO ---")
    nombre = input(" Nombre      : ")
    apellido = input(" Apellido    : ")
    especialidad = input(" Especialidad: ")
    telefono = input(" Teléfono    : ")
    v = dao.insertar(Veterinario(nombre, apellido, especialidad, telefono))
    print(f" OK Veterinario agregado con ID = {v.id}")

def agendar_cita(dao_c, dao_m, dao_v):
    print("\n--- AGENDAR CITA ---")
    try:
        mascota_id = int(input(" ID mascota: "))
        if not dao_m.buscar_por_id(mascota_id):
            raise MascotaNoEncontradaError(mascota_id)
        vet_id = int(input(" ID veterinario: "))
        if not dao_v.buscar_por_id(vet_id):
            raise VeterinarioNoEncontradoError(vet_id)
        fecha = input(" Fecha y Hora (DD-MM-YYYY HH:MM:SS): ")
        motivo = input(" Motivo: ")
        c = dao_c.insertar(Cita(mascota_id, vet_id, fecha, motivo))
        print(f" OK Cita agendada con ID = {c.id}")
    except (MascotaNoEncontradaError, VeterinarioNoEncontradoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: los IDs deben ser enteros")

def listar_duenos(dao):
    print("\n--- DUEÑOS ---")
    for d in dao.obtener_todos():
        print(f" {d}")

def listar_mascotas(dao):
    print("\n--- MASCOTAS ---")
    for m in dao.obtener_todos():
        print(f" {m}")

def listar_veterinarios(dao):
    print("\n--- VETERINARIOS ---")
    for v in dao.obtener_todos():
        print(f" {v}")

def listar_citas(dao):
    print("\n--- CITAS ---")
    for c in dao.obtener_todas():
        print(f" {c}")

def actualizar_dueno(dao):
    print("\n--- ACTUALIZAR DUEÑO ---")
    try:
        id = int(input(" ID del dueño a actualizar: "))
        nombre    = input(" Nuevo nombre    (Enter para no cambiar): ").strip()
        telefono  = input(" Nuevo teléfono  (Enter para no cambiar): ").strip()
        email     = input(" Nuevo email     (Enter para no cambiar): ").strip()
        direccion = input(" Nueva dirección (Enter para no cambiar): ").strip()
        d = dao.actualizar(id, nombre or None, telefono or None, email or None, direccion or None)
        print(f" OK Dueño actualizado: {d}")
    except (DuenoNoEncontradoError, EmailDuplicadoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")
 
def actualizar_mascota(dao):
    print("\n--- ACTUALIZAR MASCOTA ---")
    try:
        id = int(input(" ID de la mascota a actualizar: "))
        nombre = input(" Nuevo nombre (Enter para no cambiar): ").strip()
        raza   = input(" Nueva raza   (Enter para no cambiar): ").strip()
        peso_str = input(" Nuevo peso   (Enter para no cambiar): ").strip()
        peso = float(peso_str) if peso_str else None
        m = dao.actualizar(id, nombre or None, raza or None, peso)
        print(f" OK Mascota actualizada: {m}")
    except MascotaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser entero y el peso un número")

def actualizar_veterinario(dao):
    print("\n--- ACTUALIZAR VETERINARIO ---")
    try:
        id = int(input(" ID del veterinario a actualizar: "))
        especialidad = input(" Nueva especialidad (Enter para no cambiar): ").strip()
        telefono     = input(" Nuevo teléfono     (Enter para no cambiar): ").strip()
        disp_str     = input(" ¿Disponible? (s/n, Enter para no cambiar): ").strip().lower()
        disponible = None
        if disp_str == "s": disponible = True
        elif disp_str == "n": disponible = False
        v = dao.actualizar(id, especialidad or None, telefono or None, disponible)
        print(f" OK Veterinario actualizado: {v}")
    except VeterinarioNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")

def actualizar_cita(dao):
    print("\n--- CAMBIAR ESTADO DE CITA ---")
    try:
        id = int(input(" ID de la cita: "))
        print(f" Estados válidos: {Cita.E_Validos}")
        nuevo_estado = input(" Nuevo estado: ").strip().capitalize()
        c = dao.cambiar_estado(id, nuevo_estado)
        print(f" OK Cita actualizada: {c}")
    except (CitaNoEncontradaError, EstadoInvalidoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(f" ERROR: el ID debe ser un número entero")
 
def eliminar_dueno(dao):
    print("\n--- ELIMINAR DUEÑO ---")
    try:
        id = int(input(" ID del dueño a eliminar: "))
        dao.eliminar(id)
        print(f" OK Dueño ID = {id} eliminado")
    except DuenoNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")

def eliminar_mascota(dao):
    print("\n--- ELIMINAR MASCOTA ---")
    try:
        id = int(input(" ID de la mascota a eliminar: "))
        dao.eliminar(id)
        print(f" OK Mascota ID = {id} eliminada")
    except MascotaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")
 
def eliminar_veterinario(dao):
    print("\n--- ELIMINAR VETERINARIO ---")
    try:
        id = int(input(" ID del veterinario a eliminar: "))
        dao.eliminar(id)
        print(f" OK Veterinario ID = {id} eliminado")
    except VeterinarioNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")

def eliminar_cita(dao):
    print("\n--- ELIMINAR CITA ---")
    try:
        id = int(input(" ID de la cita a eliminar: "))
        dao.eliminar(id)
        print(f" OK Cita ID = {id} eliminada")
    except CitaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: el ID debe ser un número entero")

#=======================
#FUNCIONALIDADES DE JSON
#=======================

def ver_duenos_json(dao):
    print("\n--- DUEÑOS EN JSON ---")
    duenos = dao.obtener_todos()
    if duenos:
        datos = [d.to_dict() for d in duenos]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay dueños registrados)")

def ver_mascotas_json(dao):
    print("\n--- MASCOTAS EN JSON ---")
    mascotas = dao.obtener_todos()
    if mascotas:
        datos = [m.to_dict() for m in mascotas]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay mascotas registradas)")

def ver_veterinarios_json(dao):
    print("\n--- VETERINARIOS EN JSON ---")
    veterinarios = dao.obtener_todos()
    if veterinarios:
        datos = [v.to_dict() for v in veterinarios]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay veterinarios registrados)")

def ver_citas_json(dao):
    print("\n--- CITAS EN JSON ---")
    citas = dao.obtener_todas()
    if citas:
        datos = [c.to_dict() for c in citas]
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(" (No hay citas registradas)")