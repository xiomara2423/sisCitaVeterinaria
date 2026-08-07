import { useState } from "react";

function TabDuenos({ duenos = [], onCrear, onActualizar, onEliminar }) {
  const [form, setForm] = useState({ nombre: "", apellido: "", telefono: "", email: "", direccion: "" });
  const [editandoId, setEditandoId] = useState(null);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  function limpiarFormulario() {
    setForm({ nombre: "", apellido: "", telefono: "", email: "", direccion: "" });
    setEditandoId(null);
  }

  function empezarEdicion(d) {
    setEditandoId(d.id);
    setForm({ nombre: d.nombre, apellido: d.apellido, telefono: d.telefono, email: d.email, direccion: d.direccion });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const { nombre, apellido, telefono, email, direccion } = form;
    if (!nombre.trim() || !apellido.trim() || !telefono.trim() || !email.trim() || !direccion.trim()) {
      return;
    }

    const datosDueno = {
      nombre: nombre.trim(),
      apellido: apellido.trim(),
      telefono: telefono.trim(),
      email: email.trim(),
      direccion: direccion.trim(),
    };

    const exito = editandoId
      ? await onActualizar(editandoId, datosDueno)
      : await onCrear(datosDueno);

    if (!exito) return;

    limpiarFormulario();
    const modalElement = document.getElementById("modalDueno");
    const modalInstance = window.bootstrap?.Modal?.getInstance(modalElement);
    if (modalInstance) modalInstance.hide();
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="h4 d-flex align-items-center gap-2 mb-0 fw-bold">
          <span>👤</span> Dueños registrados
        </h2>
        <button
          type="button"
          className="btn btn-success fw-semibold px-3 py-2 rounded-3"
          style={{ backgroundColor: "#10B981", borderColor: "#10B981" }}
          data-bs-toggle="modal"
          data-bs-target="#modalDueno"
          onClick={limpiarFormulario}
        >
          + Agregar dueño
        </button>
      </div>

      {/* Modal único: Crear/Editar */}
      <div className="modal fade" id="modalDueno" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header border-0">
              <h1 className="modal-title fs-5">{editandoId ? "Editar Dueño" : "Agregar Dueño"}</h1>
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
                    <label className="form-label">Teléfono</label>
                    <input type="text" className="form-control" name="telefono" value={form.telefono} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Email</label>
                    <input type="email" className="form-control" name="email" placeholder="Ej. nombre@dominio.com" value={form.email} onChange={handleChange} required />
                  </div>
                  <div className="col-12">
                    <label className="form-label">Dirección</label>
                    <input type="text" className="form-control" name="direccion" value={form.direccion} onChange={handleChange} required />
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
      <div className="table-responsive ">
        <table className="table align-middle table-hover mb-0 table-bordered">
          <thead className="bg-white small fw-bold">
            <tr>
              <th className="py-3">ID</th>
              <th className="py-3">Nombre</th>
              <th className="py-3">Apellido</th>
              <th className="py-3">Teléfono</th>
              <th className="py-3">Email</th>
              <th className="py-3">Dirección</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {duenos.map((d) => (
              <tr key={d.id}>
                <td className="py-3 fw-semibold">{d.id}</td>
                <td>{d.nombre}</td>
                <td>{d.apellido}</td>
                <td>{d.telefono}</td>
                <td>{d.email}</td>
                <td>{d.direccion}</td>
                <td className="text-center">
                  <button
                    className="btn btn-sm btn-outline-secondary me-2 px-2 py-1"
                    data-bs-toggle="modal"
                    data-bs-target="#modalDueno"
                    onClick={() => empezarEdicion(d)}
                  >
                    ✏️ Editar
                  </button>
                  <button className="btn btn-sm btn-outline-danger px-2 py-1" onClick={() => onEliminar(d.id)}>
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

export default TabDuenos;