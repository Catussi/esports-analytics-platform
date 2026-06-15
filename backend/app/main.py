import os
import subprocess
import sys
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.v1 import api_v1_router

settings = get_settings()

CSV_PATH = Path(os.getenv("CSV_PATH", "/data/CSGO.csv"))


def _run_background_seed() -> None:
    if os.getenv("RUN_SEED", "false").lower() != "true":
        return

    if not CSV_PATH.exists():
        print(f"ADVERTENCIA: RUN_SEED=true pero no existe {CSV_PATH}", file=sys.stderr)
        return

    print("Seed en background: iniciando carga de CSGO.csv ...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.seed_csgo",
            "--csv-path",
            str(CSV_PATH),
            "--clear",
        ],
        check=False,
    )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if os.getenv("RUN_SEED", "false").lower() == "true":
        threading.Thread(target=_run_background_seed, daemon=True).start()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok", "docs": "/api/docs"}


@app.get("/api/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
