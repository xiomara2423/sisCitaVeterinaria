import React from "react";

const Encabezado = () => (
  <header className="d-flex justify-content-between align-items-center mb-5">
    <div>
      <h1 className="h4 m-0 text-success fw-bold d-flex align-items-baseline gap-2">
        🐾 SisCita Veterinaria RX <span className="text-muted fs-6 fw-normal">v1.0</span>
      </h1>
    </div>
    <div>
      <span className="badge rounded-pill bg-success px-3 py-2 fs-6 shadow-sm">
        Logger & SistemaConfig activos
      </span>
    </div>
  </header>
);

export default Encabezado;

