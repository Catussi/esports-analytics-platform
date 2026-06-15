from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlayerBase(BaseModel):
    steam_id: str = Field(..., min_length=5, max_length=20, examples=["76561198036987787"])
    nickname: str | None = Field(None, max_length=100)
    team: str | None = Field(None, max_length=100)
    is_active: bool = True


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    nickname: str | None = Field(None, max_length=100)
    team: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class PlayerResponse(PlayerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class PlayerListResponse(BaseModel):
    total: int
    items: list[PlayerResponse]
