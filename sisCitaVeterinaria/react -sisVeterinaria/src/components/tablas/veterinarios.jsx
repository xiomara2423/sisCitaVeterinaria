import { useState } from "react";

function TabVet({ veterinarios = [], onCrear, onActualizar, onEliminar }) {
  const [form, setForm] = useState({ nombre: "", apellido: "", especialidad: "", telefono: "", disponible: true });
  const [editandoId, setEditandoId] = useState(null);

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  function limpiarFormulario() {
    setForm({ nombre: "", apellido: "", especialidad: "", telefono: "", disponible: true });
    setEditandoId(null);
  }

  function empezarEdicion(v) {
    setEditandoId(v.id);
    setForm({ nombre: v.nombre, apellido: v.apellido, especialidad: v.especialidad, telefono: v.telefono, disponible: v.disponible });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const exito = editandoId
      ? await onActualizar(editandoId, form)
      : await onCrear(form);

    if (!exito) return;

    limpiarFormulario();

    const modalElement = document.getElementById("modalVeterinario");
    const modalInstance = window.bootstrap?.Modal?.getInstance(modalElement);
    if (modalInstance) modalInstance.hide();
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="h4 d-flex align-items-center gap-2 mb-0 fw-bold">
          <span className="text-primary">🩺</span> Veterinarios registrados
        </h2>
        <button
          type="button"
          className="btn btn-success fw-semibold px-3 py-2 rounded-3"
          style={{ 
            backgroundColor: "#10B981",
            borderColor: "#10B981" }}
          data-bs-toggle="modal"
          data-bs-target="#modalVeterinario"
          onClick={limpiarFormulario}
        >
          + Agregar veterinario
        </button>
      </div>

      {/* Modal único: Crear/Editar */}
      <div className="modal fade" id="modalVeterinario" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header border-0">
              <h1 className="modal-title fs-5">{editandoId ? "Editar Veterinario" : "Veterinario"}</h1>
              <button type="button" className="btn-close" data-bs-dismiss="modal" onClick={limpiarFormulario}></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">Nombre completo</label>
                    <input type="text" className="form-control" name="nombre" placeholder="Nombres" value={form.nombre} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">&nbsp;</label>
                    <input type="text" className="form-control" name="apellido" placeholder="Apellidos" value={form.apellido} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Especialidad</label>
                    <input type="text" className="form-control" name="especialidad" value={form.especialidad} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Teléfono</label>
                    <input type="text" className="form-control" name="telefono" value={form.telefono} onChange={handleChange} required />
                  </div>
                  <div className="col-12">
                    <div className="form-check">
                      <input className="form-check-input" type="checkbox" id="chkDisponible" name="disponible" checked={form.disponible} onChange={handleChange} />
                      <label className="form-check-label" htmlFor="chkDisponible">Disponible</label>
                    </div>
                  </div>
                </div>
              </div>
              <div className="modal-footer border-0">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" onClick={limpiarFormulario}>Cerrar</button>
                <button type="submit" className="btn btn-success">{editandoId ? "Guardar cambios" : "Crear"}</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="table-responsive">
        <table className="table align-middle table-hover mb-0 table-bordered">
          <thead className= " bg-white small fw-bold">
            <tr>
              <th className="py-3">ID</th>
              <th className="py-3">Nombre</th>
              <th className="py-3">Apellido</th>
              <th className="py-3">Especialidad</th>
              <th className="py-3">Teléfono</th>
              <th className="py-3">Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {veterinarios.map((v) => (
              <tr key={v.id}>
                <td className="py-3 fw-semibold">{v.id}</td>
                <td>{v.nombre}</td>
                <td>{v.apellido}</td>
                <td>{v.especialidad}</td>
                <td>{v.telefono}</td>
                <td>
                <span 
                  className="badge rounded-pill d-flex align-items-center gap-1 px-3 py-2 fw-bold" 
                  style={{ 
                    color: "#FFFFFF", 
                    fontSize: "13px", 
                    width: "fit-content",
                    backgroundColor: v.disponible ? "#2ecc71" : "#e74c3c" 
                  }}
                >
                  {v.disponible ? "✅ Disponible" : "⛔ No disponible"}
                </span>
                </td>
                <td className="text-center">
                  <button
                    className="btn btn-sm btn-outline-secondary me-2 px-2 py-1"
                    data-bs-toggle="modal"
                    data-bs-target="#modalVeterinario"
                    onClick={() => empezarEdicion(v)}
                  >
                    ✏️ Editar
                  </button>
                  <button className="btn btn-sm btn-outline-danger px-2 py-1" onClick={() => onEliminar(v.id)}>
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TabVet;