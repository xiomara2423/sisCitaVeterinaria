import { useState, useEffect } from 'react';
import api from './api/axios';
import Header from './components/menu/header';
import Tarjetas from './components/menu/tarjetas';
import PanelVeterinaria from './components/menu/panel';
import Historial from './components/menu/historial';
import useCitas from './hooks/useCitas';
import useDuenos from './hooks/useDuenos';
import useMascotas from './hooks/useMascotas';
import useVeterinarios from './hooks/useVeterinarios';

function App() {
  const [logs, setLogs] = useState([]);
  const [config, setConfig] = useState(null);

  const sincronizarLogs = async () => {
    const res = await api.get("/sistema/logs");
    setLogs([...res.data].reverse());
  };

  const limpiarHistorial = async () => {
    await api.delete("/sistema/logs");
    setLogs([]);
  };

  const {
    citas,
    cargar: cargarCitas,
    agregar: agregarCita,
    actualizarEstado: actualizarEstadoCita,
    eliminar: eliminarCita,
  } = useCitas(sincronizarLogs);

  const {
    duenos,
    cargar: cargarDuenos,
    agregar: agregarDueno,
    actualizar: actualizarDueno,
    eliminar: eliminarDueno,
  } = useDuenos(sincronizarLogs);

  const {
    mascotas,
    cargar: cargarMascotas,
    agregar: agregarMascota,
    actualizar: actualizarMascota,
    eliminar: eliminarMascota,
  } = useMascotas(sincronizarLogs);

  const {
    veterinarios,
    cargar: cargarVeterinarios,
    agregar: agregarVeterinario,
    actualizar: actualizarVeterinario,
    eliminar: eliminarVeterinario,
  } = useVeterinarios(sincronizarLogs);
  
  useEffect(() => {
    async function cargarDatos() {
      const [, , , , resConfig] = await Promise.all([
        cargarCitas(),
        cargarDuenos(),
        cargarMascotas(),
        cargarVeterinarios(),
        api.get("/sistema/config"),
      ]);
      setConfig(resConfig.data);
      await sincronizarLogs();
    }
    cargarDatos();
  }, []);

  //Cuerpo único de la página web(Header, Tarjetas, Panel(tablas) y Historial)
  return (
    <div style={{ backgroundColor: "#F8FAFC", minHeight: "100vh" }}>
      <div className="container p-4 text-dark">
        <Header config={config} />
        <Tarjetas duenos={duenos} mascotas={mascotas} veterinarios={veterinarios} citas={citas} />
        <PanelVeterinaria
          citas={citas}
          onCrearCita={agregarCita}
          onActualizarEstadoCita={actualizarEstadoCita}
          onEliminarCita={eliminarCita}
          duenos={duenos}
          onCrearDueno={agregarDueno}
          onActualizarDueno={actualizarDueno}
          onEliminarDueno={eliminarDueno}
          mascotas={mascotas}
          onCrearMascota={agregarMascota}
          onActualizarMascota={actualizarMascota}
          onEliminarMascota={eliminarMascota}
          veterinarios={veterinarios}
          onCrearVeterinario={agregarVeterinario}
          onActualizarVeterinario={actualizarVeterinario}
          onEliminarVeterinario={eliminarVeterinario}
        />
        <Historial logs={logs} onLimpiar={limpiarHistorial} />
      </div>
    </div>
  );
}

export default App