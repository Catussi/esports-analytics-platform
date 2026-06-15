"""Espera a que MySQL acepte conexiones antes de inicializar la app."""

from __future__ import annotations

import sys
import time

import pymysql

from app.config import get_settings

MAX_ATTEMPTS = 30
RETRY_SECONDS = 2


def wait_for_database() -> None:
    settings = get_settings()
    connect_kwargs = settings.mysql_connect_args()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            connection = pymysql.connect(
                host=settings.mysql_host,
                port=settings.mysql_port,
                user=settings.mysql_user,
                password=settings.mysql_password,
                database=settings.mysql_database,
                connect_timeout=5,
                **connect_kwargs,
            )
            connection.close()
            print(f"MySQL listo en {settings.mysql_host}:{settings.mysql_port}")
            return
        except pymysql.MySQLError as exc:
            print(
                f"Intento {attempt}/{MAX_ATTEMPTS}: MySQL no disponible ({exc}). "
                f"Reintentando en {RETRY_SECONDS}s...",
                file=sys.stderr,
            )
            time.sleep(RETRY_SECONDS)

    print("ERROR: MySQL no respondió a tiempo.", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    wait_for_database()
