"""
Pobla MySQL con jugadores y estadísticas agregadas desde CSGO.csv.

Uso (desde backend/):
    python -m scripts.seed_csgo
    python -m scripts.seed_csgo --limit 10000
    python -m scripts.seed_csgo --clear
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import MatchStats, Player
from scripts.csv_loader import aggregate_csgo_csv

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "CSGO.csv"


def clear_data(db: Session) -> None:
    db.execute(delete(MatchStats))
    db.execute(delete(Player))
    db.commit()


def seed_from_dataframe(db: Session, dataframe) -> tuple[int, int]:
    steam_ids = dataframe["steam_id"].unique().tolist()
    existing_players = {
        player.steam_id: player
        for player in db.scalars(select(Player).where(Player.steam_id.in_(steam_ids))).all()
    }

    players_created = 0
    for steam_id in steam_ids:
        if steam_id in existing_players:
            continue
        player = Player(
            steam_id=steam_id,
            nickname=f"Player_{steam_id[-4:]}",
            team=None,
            is_active=True,
        )
        db.add(player)
        existing_players[steam_id] = player
        players_created += 1

    db.flush()

    match_stats_rows: list[MatchStats] = []
    for row in dataframe.itertuples(index=False):
        player = existing_players[row.steam_id]
        match_stats_rows.append(
            MatchStats(
                player_id=player.id,
                map_name=row.map_name,
                team_side=row.team_side,
                match_external_id=row.match_external_id,
                kills=row.kills,
                deaths=row.deaths,
                assists=row.assists,
                headshots=row.headshots,
                adr=float(row.adr),
                kast=float(row.kast),
                rating=float(row.rating),
                flank_kills=row.flank_kills,
                avg_kill_distance=float(row.avg_kill_distance)
                if row.avg_kill_distance == row.avg_kill_distance
                else None,
                time_alive=float(row.time_alive),
                travelled_distance=float(row.travelled_distance),
            )
        )

    db.add_all(match_stats_rows)
    db.commit()
    return players_created, len(match_stats_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed database from CSGO.csv")
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
        help="Limitar filas del CSV (útil para pruebas rápidas)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Elimina jugadores y estadísticas antes de insertar",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.csv_path.exists():
        print(f"ERROR: No se encontró el CSV en {args.csv_path}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Leyendo y agregando datos desde {args.csv_path} ...")
    dataframe = aggregate_csgo_csv(args.csv_path, limit=args.limit)
    print(
        f"Registros agregados: {len(dataframe)} partidas | "
        f"{dataframe['steam_id'].nunique()} jugadores únicos"
    )

    db = SessionLocal()
    try:
        if args.clear:
            print("Limpiando tablas players y match_stats ...")
            clear_data(db)

        players_created, stats_created = seed_from_dataframe(db, dataframe)
        print(f"Jugadores insertados: {players_created}")
        print(f"Estadísticas de partida insertadas: {stats_created}")
        print("Seed completado correctamente.")
    except OperationalError as exc:
        print("ERROR: No se pudo conectar a MySQL.", file=sys.stderr)
        print("Asegúrate de tener Docker corriendo: docker compose up -d", file=sys.stderr)
        print(f"Detalle: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    finally:
        db.close()


if __name__ == "__main__":
    main()
