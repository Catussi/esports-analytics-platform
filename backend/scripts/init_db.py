"""
Script de inicialización de la base de datos.

Uso (desde la carpeta backend/):
    python -m scripts.init_db
"""

import sys

from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app.models import MatchStats, Player  # noqa: F401 — registra modelos en metadata


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as exc:
        print("ERROR: No se pudo conectar a MySQL.", file=sys.stderr)
        print(file=sys.stderr)
        print("Causa habitual: el servidor MySQL no está corriendo en localhost:3306.", file=sys.stderr)
        print(file=sys.stderr)
        print("Solución rápida con Docker (desde la raíz del proyecto):", file=sys.stderr)
        print("  docker compose up -d", file=sys.stderr)
        print("  cd backend", file=sys.stderr)
        print("  python -m scripts.init_db", file=sys.stderr)
        print(file=sys.stderr)
        print(f"Detalle técnico: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print("Tablas creadas correctamente: players, match_stats")


if __name__ == "__main__":
    init_db()
