function Header({ config }) {
  return (
    <header className="d-flex justify-content-between align-items-center mb-5">
      <div>
        {/* TITULO DEL PRINCIPAL*/}
        <h1 className="h4 fw-bold d-flex align-items-baseline gap-2"  style={{ color:"#0F766E" }}>
          🐾 {config?.nombre ?? "SisCita Veterinaria RX"}{" "}
          <span className="text-muted fs-6 fw-normal">v{config?.version ?? "..."}</span>
        </h1>
      </div>
      <div>
        <span className="badge rounded-pill  px-3 py-2 fs-6 shadow-sm" style={{ backgroundColor: "#10B981", borderColor: "#10B981" }}>
          Logger & SistemaConfig activos
        </span>
      </div>
    </header>
  );
}

export default Header;