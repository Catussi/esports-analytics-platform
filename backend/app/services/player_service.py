from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import MatchStats, Player
from app.schemas.match_stats import MatchStatsCreate
from app.schemas.player import PlayerCreate, PlayerUpdate


class PlayerService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_players(self, skip: int = 0, limit: int = 50) -> tuple[list[Player], int]:
        total = self.db.scalar(select(func.count()).select_from(Player)) or 0
        players = self.db.scalars(
            select(Player).order_by(Player.id).offset(skip).limit(limit)
        ).all()
        return list(players), total

    def get_player(self, player_id: int) -> Player:
        player = self.db.get(Player, player_id)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jugador con id={player_id} no encontrado.",
            )
        return player

    def get_player_by_steam_id(self, steam_id: str) -> Player | None:
        return self.db.scalar(select(Player).where(Player.steam_id == steam_id))

    def create_player(self, payload: PlayerCreate) -> Player:
        existing = self.get_player_by_steam_id(payload.steam_id)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un jugador con steam_id={payload.steam_id}.",
            )

        player = Player(**payload.model_dump())
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player

    def update_player(self, player_id: int, payload: PlayerUpdate) -> Player:
        player = self.get_player(player_id)
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(player, field, value)

        self.db.commit()
        self.db.refresh(player)
        return player

    def delete_player(self, player_id: int) -> None:
        player = self.get_player(player_id)
        self.db.delete(player)
        self.db.commit()

    def list_match_stats(
        self, player_id: int, skip: int = 0, limit: int = 50
    ) -> tuple[list[MatchStats], int]:
        self.get_player(player_id)
        total = (
            self.db.scalar(
                select(func.count())
                .select_from(MatchStats)
                .where(MatchStats.player_id == player_id)
            )
            or 0
        )
        stats = self.db.scalars(
            select(MatchStats)
            .where(MatchStats.player_id == player_id)
            .order_by(MatchStats.id.desc())
            .offset(skip)
            .limit(limit)
        ).all()
        return list(stats), total

    def create_match_stats(self, player_id: int, payload: MatchStatsCreate) -> MatchStats:
        self.get_player(player_id)
        match_stats = MatchStats(player_id=player_id, **payload.model_dump())
        self.db.add(match_stats)
        self.db.commit()
        self.db.refresh(match_stats)
        return match_stats
