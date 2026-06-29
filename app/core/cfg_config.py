from pydantic_settings import BaseSettings


def _split_origins(value: str) -> list[str]:
    """Convierte una cadena de origins separados por coma en una lista limpia."""
    if not value:
        return []
    return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]


class Settings(BaseSettings):
    # Base de datos PostgreSQL en la nube. En Render debe venir desde Environment Variables.
    DATABASE_URL: str

    # Clave JWT. En Render debes sobrescribirla con una SECRET_KEY propia.
    SECRET_KEY: str = "alfin_core_change_me_in_render_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # URL del backend del portal cliente/homebanking si alguna ruta del core lo consulta.
    PORTAL_BACKEND_URL: str = "https://santander-homebanking-backend.onrender.com"
    PORT: int = 8001

    # Dominios permitidos para CORS. Separar por comas.
    CORS_ORIGINS: str = (
        "https://santander-corefrontend.vercel.app,https://santander-core-frontend.vercel.app,https://santander-core.vercel.app,https://santander-corebanking.vercel.app,https://santander-homefront.vercel.app,https://santander-homebanking.vercel.app,https://santander-home-banking.vercel.app,http://localhost:5173,http://localhost:5174,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:3000"
    )

    # Variables compatibles con Render/Railway/Vercel si prefieres declarar un solo frontend.
    FRONTEND_URL: str = ""
    CLIENT_URL: str = ""
    CORE_FRONTEND_URL: str = ""
    HOMEBANKING_FRONTEND_URL: str = ""

    # Permite previews y dominios Vercel sin tener que agregarlos uno por uno.
    CORS_ORIGIN_REGEX: str = r"https://.*\.vercel\.app"

    @property
    def cors_origins_list(self) -> list[str]:
        origins: list[str] = []
        for value in (
            self.CORS_ORIGINS,
            self.FRONTEND_URL,
            self.CLIENT_URL,
            self.CORE_FRONTEND_URL,
            self.HOMEBANKING_FRONTEND_URL,
        ):
            origins.extend(_split_origins(value))

        # Quita duplicados preservando el orden.
        unique: list[str] = []
        for origin in origins:
            if origin not in unique:
                unique.append(origin)
        return unique

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
