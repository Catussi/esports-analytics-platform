from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MatchStatsBase(BaseModel):
    map_name: str = Field(..., min_length=1, max_length=50, examples=["de_inferno"])
    team_side: str | None = Field(None, max_length=30, examples=["Terrorist"])
    match_external_id: int | None = None

    kills: int = Field(0, ge=0)
    deaths: int = Field(0, ge=0)
    assists: int = Field(0, ge=0)
    headshots: int = Field(0, ge=0)
    adr: float = Field(0.0, ge=0.0)
    kast: float = Field(0.0, ge=0.0, le=100.0)
    rating: float = Field(0.0, ge=0.0)

    flank_kills: int = Field(0, ge=0)
    avg_kill_distance: float | None = Field(None, ge=0.0)
    time_alive: float | None = Field(None, ge=0.0)
    travelled_distance: float | None = Field(None, ge=0.0)
    played_at: datetime | None = None


class MatchStatsCreate(MatchStatsBase):
    pass


class MatchStatsResponse(MatchStatsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player_id: int
    created_at: datetime


class MatchStatsListResponse(BaseModel):
    total: int
    items: list[MatchStatsResponse]
