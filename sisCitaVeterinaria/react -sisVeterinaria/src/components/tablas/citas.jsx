import { useState } from "react";

function TabCitas({ citas = [], mascotas = [], veterinarios = [], onCrear, onActualizarEstado, onEliminar }) {
  const [fechaDia, setFechaDia] = useState("");
  const [horaCita, setHoraCita] = useState("");
  const [mascotaId, setMascotaId] = useState("");
  const [veterinarioId, setVeterinarioId] = useState("");
  const [motivo, setMotivo] = useState("");

  const nombreMascota = (id) => mascotas.find((m) => m.id === id)?.nombre ?? "—";
  const nombreVet = (id) => {
    const v = veterinarios.find((v) => v.id === id);
    return v ? `${v.nombre} ${v.apellido}` : "—";
  };

  function limpiarFormulario() {
    setFechaDia(""); setHoraCita(""); setMascotaId(""); setVeterinarioId(""); setMotivo("");
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (!fechaDia || !horaCita || !mascotaId || !veterinarioId || !motivo.trim()) {
      return;
    }

    const exito = await onCrear({
      fecha: `${fechaDia} ${horaCita}`,
      mascota_id: Number(mascotaId),
      veterinario_id: Number(veterinarioId),
      motivo: motivo.trim(),
    });

    if (!exito) return;

    limpiarFormulario();
    const modalElement = document.getElementById("modalCita");
    const modalInstance = window.bootstrap?.Modal?.getInstance(modalElement);
    if (modalInstance) modalInstance.hide();
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="h4 d-flex align-items-center gap-2 mb-0 fw-bold">
          <span>📅</span> Citas registradas
        </h2>
        <button
          type="button"
          className="btn btn-success fw-semibold px-3 py-2 rounded-3"
          style={{ backgroundColor: "#10B981", borderColor: "#10B981" }}
          data-bs-toggle="modal"
          data-bs-target="#modalCita"
          onClick={limpiarFormulario}
        >
          + Agendar cita
        </button>
      </div>

      {/* Modal: solo Crear */}
      <div className="modal fade" id="modalCita" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header border-0">
              <h1 className="modal-title fs-5">Cita</h1>
              <button type="button" className="btn-close" data-bs-dismiss="modal" onClick={limpiarFormulario}></button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">Fecha</label>
                    <input type="date" className="form-control" value={fechaDia} onChange={(e) => setFechaDia(e.target.value)} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Hora</label>
                    <input type="time" lang="es-PE" className="form-control" value={horaCita} onChange={(e) => setHoraCita(e.target.value)} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Mascota</label>
                    <select className="form-select" value={mascotaId} onChange={(e) => setMascotaId(e.target.value)} required>
                      <option disabled value="">Selecciona una mascota...</option>
                      {mascotas.map((m) => (
                        <option key={m.id} value={m.id}>{m.nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Veterinario</label>
                    <select className="form-select" value={veterinarioId} onChange={(e) => setVeterinarioId(e.target.value)} required>
                      <option disabled value="">Selecciona un veterinario...</option>
                      {veterinarios.map((v) => (
                        <option key={v.id} value={v.id}>{v.nombre} {v.apellido}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-12">
                    <label className="form-label">Motivo</label>
                    <input type="text" className="form-control" placeholder="Ej: Chequeo visual" value={motivo} onChange={(e) => setMotivo(e.target.value)} required />
                  </div>
                </div>
              </div>
              <div className="modal-footer border-0">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" onClick={limpiarFormulario}>Cerrar</button>
                <button type="submit" className="btn btn-success">Crear</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Tabla */}
      <div className="table-responsive">
        <table className="table table-bordered  align-middle table-hover mb-0">
          <thead className="bg-white text-secondary small fw-bold">
            <tr>
              <th className="py-3">ID</th>
              <th className="py-3">Fecha</th>
              <th className="py-3">Mascota</th>
              <th className="py-3">Veterinario</th>
              <th className="py-3">Motivo</th>
              <th className="py-3">Estado</th>
              <th></th>
            </tr>
          </thead>
       {/*diseño de registros*/}
          <tbody>
            {citas.map((c) => (
              <tr key={c.id}>
                {/* negrita [fw-semibold]*/}
                <td >{c.id}</td>
                <td>{c.fecha}</td>
                <td>{nombreMascota(c.mascota_id)}</td>
                <td>{nombreVet(c.veterinario_id)}</td>
                <td>{c.motivo}</td>
                <td>
                   {/* color de boton de estado*/}
                  <select 
                    className="form-select form-select-sm " style={{backgroundColor:"#D9D9D9"}}
                    value={c.estado}
                    onChange={(e) => onActualizarEstado(c.id, e.target.value)}
                  >
                    <option className="bg-white" value="Programada">Programada</option>
                    <option className="bg-white" value="Completada">Completada</option>
                    <option className="bg-white" value="Cancelada">Cancelada</option>
                  </select>
                </td>
               <td>
                  <div className="d-flex align-items-center justify-content-center gap-3">
                    <span
                      className="badge rounded-pill d-flex align-items-center gap-1 px-3 py-2 fw-bold" 
                      style={{ color: '#ffffff', fontSize: '13px' ,backgroundColor:"#0f766e" }}
                    >
                      ⏱ {c.estado}
                    </span>
                    <button className="btn btn-outline-danger btn-sm d-flex align-items-center gap-1 px-3 py-1" 
                    onClick={()=>onEliminar(c.id)}>
                      🗑 Eliminar
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TabCitas;