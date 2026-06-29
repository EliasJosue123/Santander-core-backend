from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cfg_config import settings
from app.routes import (
    rtr_scoring,
    rtr_creditos,
    rtr_ahorros,
    rtr_dashboard,
    rtr_clientes,
    rtr_auth,
    rtr_homebanking,
    rtr_recuperaciones,
)

app = FastAPI(
    title="Core Financiero — Banco Andino",
    description="Motor de scoring, cartera crediticia y KPIs institucionales",
    version="1.0.0",
)

# CORS para desarrollo local, producción en Vercel y previews de Vercel.
# Si tu dominio final cambia, puedes agregarlo en Render como CORS_ORIGINS.
cors_origins = settings.cors_origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(rtr_auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rtr_scoring.router, prefix="/scoring", tags=["Scoring"])
app.include_router(rtr_creditos.router, prefix="/creditos", tags=["Créditos"])
app.include_router(rtr_ahorros.router, prefix="/ahorros", tags=["Ahorros"])
app.include_router(rtr_clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(rtr_dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(rtr_homebanking.router, prefix="/hb", tags=["Homebanking"])
app.include_router(rtr_recuperaciones.router, prefix="/recuperaciones", tags=["Recuperaciones"])


@app.get("/", tags=["root"])
def root():
    return {
        "sistema": "Core Financiero Banco Andino",
        "version": "1.0.0",
        "status": "ok",
        "docs": "/docs",
        "puerto": settings.PORT,
        "cors": cors_origins,
    }
