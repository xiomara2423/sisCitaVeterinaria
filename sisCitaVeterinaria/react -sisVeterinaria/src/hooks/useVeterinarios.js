import { useState } from "react";
import api from "../api/axios";

function useVeterinarios(sincronizarLogs) {
  const [veterinarios, setVeterinarios] = useState([]);
  
  

  const cargar = async () => {
    const res = await api.get("/veterinarios/");
    setVeterinarios(res.data);
  };

  {/* metodo http post para agregar, crear veterinarios */}
  const agregar = async (nuevo) => {
    try {
      const res = await api.post("/veterinarios/", nuevo);
      setVeterinarios((prev) => [...prev, res.data]);
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

   {/* metodo http put para actualizar veterinarios */}
  const actualizar = async (id, datos) => {
    try {
      const res = await api.put(`/veterinarios/${id}`, datos);
      setVeterinarios((prev) => prev.map((v) => (v.id === id ? res.data : v)));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  {/* metodo http delete  para eliminar veterinarios */}
  const eliminar = async (id) => {
    try {
      await api.delete(`/veterinarios/${id}`);
      setVeterinarios((prev) => prev.filter((v) => v.id !== id));
      await sincronizarLogs();
      return true;
    } catch (error) {
      await sincronizarLogs();
      return false;
    }
  };

  return { veterinarios, cargar, agregar, actualizar, eliminar };
}

export default useVeterinarios;