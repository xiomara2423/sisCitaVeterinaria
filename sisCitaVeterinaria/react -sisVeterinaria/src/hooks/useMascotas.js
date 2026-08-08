import { useState } from "react";
import api from "../api/axios";

function useMascotas(sincronizarLogs) {
  const [mascotas, setMascotas] = useState([]);

  const cargar = async () => {
    const res = await api.get("/mascotas/");
    setMascotas(res.data);
  };

{/* metodo http post  para agregar, crear mascotas */}

  const agregar = async (nuevo) => {
    try {
      const res = await api.post("/mascotas/", nuevo);
      setMascotas((prev) => [...prev, res.data]);
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

 {/* metodo http put  para actualizar mascotas */}

  const actualizar = async (id, { nombre, raza, peso }) => {
    try {
      const res = await api.put(`/mascotas/${id}`, { nombre, raza, peso });
      setMascotas((prev) => prev.map((m) => (m.id === id ? res.data : m)));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

{/* metodo http delete  para eliminar  mascotas */}

  const eliminar = async (id) => {
    try {
      await api.delete(`/mascotas/${id}`);
      setMascotas((prev) => prev.filter((m) => m.id !== id));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  return { mascotas, cargar, agregar, actualizar, eliminar };
}

export default useMascotas;