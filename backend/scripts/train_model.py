"""
Entrena el pipeline StandardScaler -> PCA -> K-Means con CSGO.csv.

Uso (desde backend/):
    python -m scripts.train_model
    python -m scripts.train_model --limit 5000
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app.config import get_settings
from app.ml.training import save_pipeline, train_clustering_pipeline
from scripts.csv_loader import aggregate_csgo_csv

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "CSGO.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Entrena modelo K-Means/PCA para CS:GO")
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Ruta al archivo CSGO.csv",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limitar filas del CSV para entrenamiento rápido",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Ruta de salida del modelo .joblib",
    )
    parser.add_argument(
        "--clusters",
        type=int,
        default=4,
        help="Número de clústeres K-Means",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    output_path = args.output or Path(settings.ml_model_path)

    if not args.csv_path.exists():
        print(f"ERROR: No se encontró el CSV en {args.csv_path}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Cargando dataset desde {args.csv_path} ...")
    dataframe = aggregate_csgo_csv(args.csv_path, limit=args.limit)
    print(f"Muestras de entrenamiento: {len(dataframe)}")

    pipeline = train_clustering_pipeline(dataframe, n_clusters=args.clusters)
    save_pipeline(pipeline, output_path)

    explained = pipeline["explained_variance_ratio"]
    print(f"Modelo guardado en: {output_path}")
    print(f"Varianza explicada por PCA: {[round(v, 4) for v in explained]}")
    print("Perfiles de clúster:")
    for cluster_id, profile in sorted(pipeline["cluster_profiles"].items()):
        print(f"  [{cluster_id}] {profile['label']}")


if __name__ == "__main__":
    main()
