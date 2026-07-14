
# SisCitaVeterinaria 
Sistema de Gestión de Citas para la VeterinariaRX desarrollado en Python utilizando Programación Orientada a Objetos (POO).

---------------------------------Descripción del Proyecto-------------------------------

Este proyecto esta diseñada para automatizar y administrar los procesos esenciales en una veterinaria: el registro de dueños, el historial de las mascotas, la asignación de veterinarios y el control de las citas médicas. 

## El sistema se organiza en base a cuatro entidades que interactúan entre sí:

1. Dueño
Administra los datos de contacto de los clientes de la clínica.

2. Mascota 
Modela a los pacientes que reciben atención médica y se vincula directamente a un dueño mediante su ID.

3. Veterinario 
Representa al personal médico responsable del diagnóstico y tratamiento de las mascotas.

4. Cita 
Es el núcleo del sistema, encargada de entrelazar de forma coordinada a una *Mascota*, un *Veterinario*, un motivo de consulta y una fecha específica.