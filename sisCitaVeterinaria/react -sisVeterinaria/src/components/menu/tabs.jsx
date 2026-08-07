//controla los nombres aca y en panel.jsx de los tabs la parte baja 
const tabs = [
  { key: "citas", label: "Citas", icon: "📅" },
  { key: "duenos", label: "Dueños", icon: "👤" },
  { key: "mascotas", label: "Mascotas", icon: "🐾" },
  { key: "veterinarios", label: "Veterinarios", icon: "🩺" },
];


const Tabs = ({ vistaActiva, setVistaActiva }) => {
  return (
    //centra el titulo de los navegadores
    <ul className="nav nav-tabs mb-4">
      {tabs.map((tab) => (
        <li className="nav-item" key={tab.key}>
          <button
            className={`nav-link d-flex align-items-center gap-2 ${
              vistaActiva === tab.key 
                ? "active text-success fw-bold"
                : "text-secondary fw-semibold"
            }`}
            onClick={() => setVistaActiva(tab.key)}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        </li>
      ))}
    </ul>
  );
};

export default Tabs;