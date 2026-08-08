function Historial({ logs = [], onLimpiar }) {
  return (
    <div className="card border-0 mt-4">
         <div className="card-header d-flex justify-content-between align-items-center pb-2 border-bottom " style={{backgroundColor:"#f1f5f9"}}>
      
        <h2 className="h4 fw-bold text-success ">📋 Historial del sistema — Logger()</h2>
        <button className="btn btn-outline-primary btn-sm fw-medium  " onClick={onLimpiar}>✏️ Limpiar historial</button>
      </div>

        <div className="card-body pt-1">
          {logs.length === 0 && (
            <p className="text-muted small mb-0">Sin eventos registrados.</p>
          )}
          {logs.map((log, i) => (
            <div key={i} className="d-flex align-items-center  py-2 gap-3 border-bottom small">
              <span className="text-muted" style={{ minWidth: "70px" }}>{log.hora}</span>
              <span
                className={`badge ${
                  log.nivel === "ERROR"
                    ? "bg-danger"
                    : log.nivel === "WARNING"
                    ? "bg-warning text-dark"
                    : "bg-success"
                }`}
                style={{ minWidth: "60px" }}
              >
                {log.nivel}
              </span>
              <span>{log.msg}</span>
            </div>
          ))}
        </div>
      </div>
    
  );
}

export default Historial;