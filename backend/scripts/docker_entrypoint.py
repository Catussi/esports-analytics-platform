"""
Entrypoint rápido: espera DB, crea tablas y arranca Uvicorn.
Seed opcional corre en background vía lifespan de FastAPI.
"""

from __future__ import annotations

import os

from scripts.init_db import init_db
from scripts.wait_for_db import wait_for_database


def _resolve_port() -> str:
    explicit = os.getenv("PORT")
    if explicit:
        return explicit
    if os.getenv("APP_ENV", "").lower() == "production":
        return "10000"
    return "8000"


def main() -> None:
    wait_for_database()
    init_db()

    port = _resolve_port()
    print(f"Iniciando Uvicorn en 0.0.0.0:{port} (PORT env={os.getenv('PORT', 'no definido')})")

    os.execvp(
        "uvicorn",
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port],
    )


if __name__ == "__main__":
    main()
