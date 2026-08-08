from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Config.base_datos import inicializar
from routers import Citas, Duenos, Mascotas, Veterinarios, Sistemas
from Config.sistema_config import SistemaConfig

app = FastAPI(
    title="Sistema de Citas Veterinaria RX",
    version="1.0",
    description="API REST para agendar citas médicas de mascotas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()
sc = SistemaConfig()

app.include_router(Citas.router)
app.include_router(Duenos.router)
app.include_router(Mascotas.router)
app.include_router(Veterinarios.router)
app.include_router(Sistemas.router)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema de Citas Veterinaria RX",
            "version": "1.0",
            "docs": "/docs"
    }