import json
from Modelos.Dueno import Dueno
from Modelos.Mascota import Mascota
from Modelos.Veterinario import Veterinario
from Modelos.Cita import Cita
import os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_DUENOS = os.path.join(_BASE, "datos_duenos.json")
ARCHIVO_MASCOTAS = os.path.join(_BASE, "datos_mascotas.json")
ARCHIVO_VETERINARIOS = os.path.join(_BASE, "datos_veterinarios.json")
ARCHIVO_CITAS = os.path.join(_BASE, "datos_citas.json")

#====================
#PERSISTENCIA EN JSON
#====================

def guardar_duenos(ddao):

    datos = [d.to_dict() for d in ddao.obtener_todos()]
    
    with open(ARCHIVO_DUENOS, "w", encoding="utf-8") as f:

        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f" OK Dueños guardados en '{ARCHIVO_DUENOS}'")

def cargar_duenos(ddao):
    try:
        with open(ARCHIVO_DUENOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            dueno = Dueno.from_dict(d)
            ddao._DuenoDAO__bd.append(dueno)
            if dueno.id >= ddao._DuenoDAO__cid:
                ddao._DuenoDAO__cid = dueno.id + 1
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_DUENOS}', se empieza desde cero")

def guardar_mascotas(mdao):
    datos = [m.to_dict() for m in mdao.obtener_todos()]

    with open(ARCHIVO_MASCOTAS, "w", encoding="utf-8") as f:

        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f" OK Mascotas guardadas en '{ARCHIVO_MASCOTAS}'")

def cargar_mascotas(mdao):
    try:
        with open(ARCHIVO_MASCOTAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            mascota = Mascota.from_dict(d)
            mdao._MascotaDAO__bd.append(mascota)
            if mascota.id >= mdao._MascotaDAO__mid:
                mdao._MascotaDAO__mid = mascota.id + 1
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_MASCOTAS}', se empieza desde cero")

def guardar_veterinarios(vdao):
    datos = [v.to_dict() for v in vdao.obtener_todos()]

    with open(ARCHIVO_VETERINARIOS, "w", encoding="utf-8") as f:

        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f" OK Veterinarios guardados en '{ARCHIVO_VETERINARIOS}'")

def cargar_veterinarios(vdao):
    try:
        with open(ARCHIVO_VETERINARIOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            vet = Veterinario.from_dict(d)
            vdao._VeterinarioDAO__bd.append(vet)
            if vet.id >= vdao._VeterinarioDAO__vid:
                vdao._VeterinarioDAO__vid = vet.id + 1
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_VETERINARIOS}', se empieza desde cero")

def guardar_citas(cdao):
    datos = [c.to_dict() for c in cdao.obtener_todas()]

    with open(ARCHIVO_CITAS, "w", encoding="utf-8") as f:

        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f" OK Citas guardadas en '{ARCHIVO_CITAS}'")

def cargar_citas(cdao):
    try:
        with open(ARCHIVO_CITAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            cita = Cita.from_dict(d)
            cdao._CitaDAO__bd.append(cita)
            if cita.id >= cdao._CitaDAO__cid:
                cdao._CitaDAO__cid = cita.id + 1
    except FileNotFoundError:
        print(f" AVISO: No existe '{ARCHIVO_CITAS}', se empieza desde cero")