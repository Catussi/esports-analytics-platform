"""
Carga y agrega el dataset CSGO.csv (nivel round) a registros por jugador/partida.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _parse_survived(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def aggregate_csgo_csv(csv_path: Path, limit: int | None = None) -> pd.DataFrame:
    read_kwargs: dict = {"sep": ";", "low_memory": False}
    if limit is not None:
        read_kwargs["nrows"] = limit

    raw = pd.read_csv(csv_path, **read_kwargs)
    survived = _parse_survived(raw["Survived"])

    aggregated = (
        raw.assign(_survived=survived)
        .groupby(["SteamId", "MatchId"], as_index=False)
        .agg(
            map_name=("Map", "first"),
            team_side=("Team", "first"),
            rounds_played=("RoundId", "max"),
            kills=("MatchKills", "last"),
            assists=("MatchAssists", "last"),
            headshots=("MatchHeadshots", "last"),
            flank_kills=("MatchFlankKills", "last"),
            avg_kill_distance=("AvgMatchKillDist", "last"),
            time_alive=("TimeAlive", "sum"),
            travelled_distance=("TravelledDistance", "sum"),
            survived_rounds=("_survived", "sum"),
            round_kills=("RoundKills", "sum"),
            round_assists=("RoundAssists", "sum"),
        )
    )

    impact = (
        raw.assign(_survived=survived)
        .groupby(["SteamId", "MatchId"])
        .apply(
            lambda group: (
                (group["RoundKills"] > 0)
                | (group["RoundAssists"] > 0)
                | group["_survived"]
            ).sum(),
            include_groups=False,
        )
        .reset_index(name="impact_rounds")
    )
    aggregated = aggregated.merge(impact, on=["SteamId", "MatchId"])

    aggregated["deaths"] = (aggregated["rounds_played"] - aggregated["survived_rounds"]).clip(lower=0)
    aggregated["adr"] = (
        (aggregated["round_kills"] * 100 + aggregated["round_assists"] * 50)
        / aggregated["rounds_played"].clip(lower=1)
    ).round(2)
    aggregated["kast"] = (
        aggregated["impact_rounds"] / aggregated["rounds_played"].clip(lower=1) * 100
    ).round(2)
    aggregated["rating"] = (
        1.0
        + (aggregated["kills"] - aggregated["deaths"]) / aggregated["rounds_played"].clip(lower=1) * 0.35
        + aggregated["assists"] / aggregated["rounds_played"].clip(lower=1) * 0.15
    ).round(2)

    aggregated["steam_id"] = aggregated["SteamId"].astype(str)
    aggregated["match_external_id"] = aggregated["MatchId"].astype(int)
    aggregated["kills"] = aggregated["kills"].astype(int)
    aggregated["deaths"] = aggregated["deaths"].astype(int)
    aggregated["assists"] = aggregated["assists"].astype(int)
    aggregated["headshots"] = aggregated["headshots"].astype(int)
    aggregated["flank_kills"] = aggregated["flank_kills"].astype(int)

    return aggregated[
        [
            "steam_id",
            "match_external_id",
            "map_name",
            "team_side",
            "kills",
            "deaths",
            "assists",
            "headshots",
            "adr",
            "kast",
            "rating",
            "flank_kills",
            "avg_kill_distance",
            "time_alive",
            "travelled_distance",
        ]
    ]
