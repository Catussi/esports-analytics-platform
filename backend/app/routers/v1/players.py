from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.match_stats import MatchStatsCreate, MatchStatsListResponse, MatchStatsResponse
from app.schemas.player import PlayerCreate, PlayerListResponse, PlayerResponse, PlayerUpdate
from app.services.player_service import PlayerService

router = APIRouter(prefix="/players", tags=["Players"])


def get_player_service(db: Session = Depends(get_db)) -> PlayerService:
    return PlayerService(db)


@router.get("", response_model=PlayerListResponse)
def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: PlayerService = Depends(get_player_service),
) -> PlayerListResponse:
    players, total = service.list_players(skip=skip, limit=limit)
    return PlayerListResponse(total=total, items=players)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service),
) -> PlayerResponse:
    return service.get_player(player_id)


@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(
    payload: PlayerCreate,
    service: PlayerService = Depends(get_player_service),
) -> PlayerResponse:
    return service.create_player(payload)


@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int,
    payload: PlayerUpdate,
    service: PlayerService = Depends(get_player_service),
) -> PlayerResponse:
    return service.update_player(player_id, payload)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service),
) -> None:
    service.delete_player(player_id)


@router.get("/{player_id}/stats", response_model=MatchStatsListResponse)
def list_player_match_stats(
    player_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: PlayerService = Depends(get_player_service),
) -> MatchStatsListResponse:
    stats, total = service.list_match_stats(player_id, skip=skip, limit=limit)
    return MatchStatsListResponse(total=total, items=stats)


@router.post(
    "/{player_id}/stats",
    response_model=MatchStatsResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_player_match_stats(
    player_id: int,
    payload: MatchStatsCreate,
    service: PlayerService = Depends(get_player_service),
) -> MatchStatsResponse:
    return service.create_match_stats(player_id, payload)
