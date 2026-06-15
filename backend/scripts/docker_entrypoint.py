"""
Entrypoint del contenedor Docker: espera DB, init, seed/train opcional y arranca Uvicorn.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from scripts.init_db import init_db
from scripts.wait_for_db import wait_for_database

CSV_PATH = Path(os.getenv("CSV_PATH", "/data/CSGO.csv"))
MODEL_PATH = Path(os.getenv("ML_MODEL_PATH", "app/ml/models/kmeans_pca_model.joblib"))


def _run(command: list[str]) -> None:
    print(f"Ejecutando: {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    wait_for_database()
    init_db()

    if os.getenv("RUN_TRAIN_MODEL", "true").lower() == "true" and not MODEL_PATH.exists():
        if not CSV_PATH.exists():
            print(f"ADVERTENCIA: CSV no encontrado en {CSV_PATH}; se omite entrenamiento.", file=sys.stderr)
        else:
            _run(
                [
                    sys.executable,
                    "-m",
                    "scripts.train_model",
                    "--csv-path",
                    str(CSV_PATH),
                    "--output",
                    str(MODEL_PATH),
                ]
            )

    if os.getenv("RUN_SEED", "false").lower() == "true":
        if not CSV_PATH.exists():
            print(f"ERROR: RUN_SEED=true pero no existe {CSV_PATH}", file=sys.stderr)
            raise SystemExit(1)
        _run(
            [
                sys.executable,
                "-m",
                "scripts.seed_csgo",
                "--csv-path",
                str(CSV_PATH),
                "--clear",
            ]
        )

    os.execvp(
        "uvicorn",
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
    )


if __name__ == "__main__":
    main()
