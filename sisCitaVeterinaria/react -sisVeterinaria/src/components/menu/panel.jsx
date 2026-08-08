import { useState } from "react";
import Tabs from "../menu/tabs";
import TabDuenos from "../tablas/duenos";
import TabMascotas from "../tablas/mascotas";
import TabVet from "../tablas/veterinarios";
import TabCitas from "../tablas/citas";


function PanelVeterinaria({
  duenos = [], mascotas = [], veterinarios = [], citas = [],
  onCrearCita, onActualizarEstadoCita, onEliminarCita,
  onCrearDueno, onActualizarDueno, onEliminarDueno,
  onCrearMascota, onActualizarMascota, onEliminarMascota,
  onCrearVeterinario, onActualizarVeterinario, onEliminarVeterinario
}) {
  // controla la vista de la primera tabla que 
  // quieres mostrar cuando actualizas la pestaña
  const [vistaActiva, setVistaActiva] = useState("citas");

  const renderTabla = () => {
    switch (vistaActiva) {
      case "citas":
        return (
          <TabCitas
            citas={citas}
            mascotas={mascotas}
            veterinarios={veterinarios}
            onCrear={onCrearCita}
            onActualizarEstado={onActualizarEstadoCita}
            onEliminar={onEliminarCita}
          />
        );
      case "duenos":
        return (
          <TabDuenos
            duenos={duenos}
            onCrear={onCrearDueno}
            onActualizar={onActualizarDueno}
            onEliminar={onEliminarDueno}
          />
        );
      case "mascotas":
        return (
          <TabMascotas
            mascotas={mascotas}
            duenos={duenos}
            onCrear={onCrearMascota}
            onActualizar={onActualizarMascota}
            onEliminar={onEliminarMascota}
          />
        );
      case "veterinarios":
        return (
          <TabVet
            veterinarios={veterinarios}
            onCrear={onCrearVeterinario}
            onActualizar={onActualizarVeterinario}
            onEliminar={onEliminarVeterinario}
          />
        );
    }
  };

  return (
    <div>
      <Tabs vistaActiva={vistaActiva} setVistaActiva={setVistaActiva} />
      <div>
        {renderTabla()}
      </div>
    </div>
  );
}

export default PanelVeterinaria;