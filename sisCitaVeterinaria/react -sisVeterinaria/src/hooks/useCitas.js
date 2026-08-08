import { useState } from "react";
import api from "../api/axios";

function useCitas(sincronizarLogs) {
  const [citas, setCitas] = useState([]);

  const cargar = async () => {
    const res = await api.get("/citas/");
    setCitas(res.data);
  };

   {/* metodo http post  para agregar, crear  citas */}

  const agregar = async (nueva) => {
    try {
      await api.post("/citas/", nueva);
      await cargar();
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };
 {/* metodo http put  para actualizar el estado de cita */}

  const actualizarEstado = async (id, nuevoEstado) => {
    try {
      const res = await api.put(`/citas/${id}`, { estado: nuevoEstado });
      setCitas((prev) => prev.map((c) => (c.id === id ? res.data : c)));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

   {/* metodo http delete  para eliminar  citas */}

  const eliminar = async (id) => {
    try {
      await api.delete(`/citas/${id}`);
      setCitas((prev) => prev.filter((c) => c.id !== id));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  return { citas, cargar, agregar, actualizarEstado, eliminar };
}

export default useCitas;