import { useState } from "react";

function TabMascotas({ mascotas = [], duenos = [], onCrear, onActualizar, onEliminar }) {
  const [form, setForm] = useState({ dueno_id: "", nombre: "", especie: "", raza: "", sexo: "", peso: "" });
  const [editandoId, setEditandoId] = useState(null);

  const nombreDueno = (id) => {
    const d = duenos.find((d) => d.id === id);
    return d ? `${d.nombre} ${d.apellido}` : "—";
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  function limpiarFormulario() {
    setForm({ dueno_id: "", nombre: "", especie: "", raza: "", sexo: "", peso: "" });
    setEditandoId(null);
  }

  function empezarEdicion(m) {
    setEditandoId(m.id);
    setForm({
      dueno_id: m.dueno_id,
      nombre: m.nombre,
      especie: m.especie,
      raza: m.raza || "",
      sexo: m.sexo || "",
      peso: m.peso ?? "",
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    let exito;
    if (editandoId) {
      // Solo se envían los campos editables
      exito = await onActualizar(editandoId, {
        nombre: form.nombre.trim(),
        raza: form.raza.trim() || null,
        peso: form.peso === "" ? null : Number(form.peso),
      });
    } else {
      exito = await onCrear({
        dueno_id: Number(form.dueno_id),
        nombre: form.nombre.trim(),
        especie: form.especie.trim(),
        raza: form.raza.trim() || null,
        sexo: form.sexo || null,
        peso: form.peso === "" ? null : Number(form.peso),
      });
    }

    if (!exito) return;

    limpiarFormulario();
    const modalElement = document.getElementById("modalMascota");
    const modalInstance = window.bootstrap?.Modal?.getInstance(modalElement);
    if (modalInstance) modalInstance.hide();
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="h4 d-flex align-items-center gap-2 mb-0 fw-bold">
          <span>🐾</span> Mascotas registradas
        </h2>
        <button
          type="button"
          className="btn btn-success fw-semibold px-3 py-2 rounded-3"
          style={{ backgroundColor: "#10B981", borderColor: "#10B981" }}
          data-bs-toggle="modal"
          data-bs-target="#modalMascota"
          onClick={limpiarFormulario}
        >
          + Agregar mascota
        </button>
      </div>

      {/* Modal único: Crear/Editar " FORMULARIO" */}
      <div className="modal fade" id="modalMascota" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header border-0">
              <h1 className="modal-title fs-5">{editandoId ? "Editar Mascota" : "Mascota"}</h1>
              <button type="button" className="btn-close" data-bs-dismiss="modal" onClick={limpiarFormulario}></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">Nombre</label>
                    <input type="text" className="form-control" name="nombre" value={form.nombre} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Especie</label>
                    <input
                      type="text" className="form-control" name="especie"
                      placeholder="Ej. Perro"
                      value={form.especie} onChange={handleChange}
                      required disabled={!!editandoId}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Raza</label>
                    <input type="text" className="form-control" name="raza" value={form.raza} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Sexo</label>
                    <input
                      type="text" className="form-control" name="sexo"
                      placeholder="M o H"
                      value={form.sexo} onChange={handleChange}
                      disabled={!!editandoId}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Peso (kg)</label>
                    <input type="number" step="0.01" min="0" className="form-control" name="peso" value={form.peso} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Dueño</label>
                    <select
                      className="form-select" name="dueno_id"
                      value={form.dueno_id} onChange={handleChange}
                      required disabled={!!editandoId}
                    >
                      <option disabled value="">Selecciona un dueño...</option>
                      {duenos.map((d) => (
                        <option key={d.id} value={d.id}>{d.nombre} {d.apellido}</option>
                      ))}
                    </select>
                  </div>
                </div>
                {editandoId && (
                  <p className="text-muted small mt-3 mb-0">
                    Especie, sexo y dueño no se pueden modificar tras el registro.
                  </p>
                )}
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
              <th className="py-3">Especie</th>
              <th className="py-3">Raza</th>
              <th className="py-3">Sexo</th>
              <th className="py-3">Peso</th>
              <th className="py-3">Dueño</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {mascotas.map((m) => (
              <tr key={m.id}>
                <td className="py-3 fw-semibold">{m.id}</td>
                <td>{m.nombre}</td>
                <td>{m.especie}</td>
                <td>{m.raza || "—"}</td>
                <td>{m.sexo || "—"}</td>
                <td>{m.peso != null ? `${m.peso} kg` : "—"}</td>
                <td>{nombreDueno(m.dueno_id)}</td>
                <td className="text-center">
                  <button
                    className="btn btn-sm btn-outline-secondary me-2 px-2 py-1"
                    data-bs-toggle="modal"
                    data-bs-target="#modalMascota"
                    onClick={() => empezarEdicion(m)}
                  >
                    ✏️ Editar
                  </button>
                  <button className="btn btn-sm btn-outline-danger px-2 py-1" onClick={() => onEliminar(m.id)}>
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

export default TabMascotas;