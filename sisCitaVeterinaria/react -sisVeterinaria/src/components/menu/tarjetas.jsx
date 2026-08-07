function Tarjetas({ duenos = [], mascotas = [], veterinarios = [], citas = [] }) {
    // Datos de las tarjetas
    const datos = [
        { id: 1, icono: "👤", cantidad: duenos.length, texto: "Dueños" },
        { id: 2, icono: "🐾", cantidad: mascotas.length, texto: "Mascotas" },
        { id: 3, icono: "🩺", cantidad: veterinarios.length, texto: "Veterinarios" },
        { id: 4, icono: "📅", cantidad: citas.filter(c => c.estado === "Programada").length, texto: "Citas programadas" }
    ];

    return (
        <section className="row g-3 my-4">
            {/*Estilos de las tarjetas*/}
            {datos.map((t) => (
                <div key={t.id} className="col-md-3">
                    <div className="card h-100 text-center bg-white border border-light-subtle border-2 rounded-3">
                        <div className="card-body d-flex flex-column justify-content-center py-4">
                            <div className="d-flex justify-content-center align-items-center gap-2 mb-2">
                                <div className="fs-3 lh-1">{t.icono}</div>
                                <h2 className="card-title h3 mb-0 fw-bold">{t.cantidad}</h2>
                            </div>
                            <p className="card-text text-muted small mb-0">{t.texto}</p>
                        </div>
                    </div>
                </div>
            ))}
        </section>
    );
}

export default Tarjetas;