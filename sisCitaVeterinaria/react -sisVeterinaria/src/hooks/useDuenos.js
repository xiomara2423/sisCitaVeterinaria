import { useState } from "react";
import api from "../api/axios";

function useDuenos(sincronizarLogs) {
  const [duenos, setDuenos] = useState([]);
  
  {/* metodo http get*/}
  const cargar = async () => {
    const res = await api.get("/duenos/");
    setDuenos(res.data);
  };

  {/* metodo http post  para agregar, crear dueños */}
  const agregar = async (nuevo) => {
    try {
      const res = await api.post("/duenos/", nuevo);
      setDuenos((prev) => [...prev, res.data]);
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

   {/* metodo http put para actualizar los campos de los dueños*/}
  const actualizar = async (id, datos) => {
    try {
      const res = await api.put(`/duenos/${id}`, datos);
      setDuenos((prev) => prev.map((d) => (d.id === id ? res.data : d)));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  {/* metodo http delete  para eliminar dueños*/}
  const eliminar = async (id) => {
    try {
      await api.delete(`/duenos/${id}`);
      setDuenos((prev) => prev.filter((d) => d.id !== id));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  return { duenos, cargar, agregar, actualizar, eliminar };
}

export default useDuenos;