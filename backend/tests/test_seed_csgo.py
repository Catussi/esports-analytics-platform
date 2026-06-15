from pathlib import Path

import pandas as pd
import pytest

from scripts.csv_loader import aggregate_csgo_csv

CSV_PATH = Path(__file__).resolve().parents[2] / "CSGO.csv"


@pytest.mark.skipif(not CSV_PATH.exists(), reason="CSGO.csv no disponible")
def test_aggregate_csgo_csv_returns_expected_columns():
    dataframe = aggregate_csgo_csv(CSV_PATH, limit=2000)

    expected_columns = {
        "steam_id",
        "match_external_id",
        "map_name",
        "kills",
        "deaths",
        "assists",
        "headshots",
        "adr",
        "kast",
        "rating",
    }
    assert expected_columns.issubset(set(dataframe.columns))
    assert len(dataframe) > 0
    assert (dataframe["deaths"] >= 0).all()
    assert (dataframe["kast"] >= 0).all()
    assert (dataframe["kast"] <= 100).all()


def test_aggregate_csgo_csv_metric_ranges_on_synthetic_sample(tmp_path: Path):
    csv_content = """id;Map;Team;InternalTeamId;MatchId;RoundId;SteamId;RoundWinner;MatchWinner;Survived;AbnormalMatch;TimeAlive;ScaledTimeAlive;AvgCentroidDistance;TravelledDistance;AvgRoundVelocity;AvgKillDistance;AvgSiteDistance;RLethalGrenadesThrown;RNonLethalGrenadesThrown;PrimaryAssaultRifle;PrimarySniperRifle;PrimaryHeavy;PrimarySMG;PrimaryPistol;FirstKillTime;RoundKills;RoundAssists;RoundHeadshots;RoundFlankKills;RoundStartingEquipmentValue;TeamStartingEquipmentValue;MatchKills;MatchFlankKills;MatchAssists;MatchHeadshots;AvgMatchKillDist
1;de_inferno;Terrorist;1;1;1;111;True;True;False;False;10;1;1;100;1;0;1;0;0;0;0;0;0;1;0;1;0;0;0;100;500;1;0;0;0;200
2;de_inferno;Terrorist;1;1;2;111;True;True;True;False;20;1;1;150;1;0;1;0;0;0;0;0;0;1;0;0;1;0;0;100;500;1;0;1;0;200
"""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    dataframe = aggregate_csgo_csv(csv_file)
    row = dataframe.iloc[0]

    assert row["steam_id"] == "111"
    assert row["kills"] == 1
    assert row["deaths"] == 1
    assert row["assists"] == 1
    assert row["headshots"] == 0
    assert row["adr"] == pytest.approx(75.0)
    assert row["kast"] == pytest.approx(100.0)
