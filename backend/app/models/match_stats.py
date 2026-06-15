from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MatchStats(Base):
    __tablename__ = "match_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    map_name: Mapped[str] = mapped_column(String(50), nullable=False)
    team_side: Mapped[str | None] = mapped_column(String(30))
    match_external_id: Mapped[int | None] = mapped_column(Integer, index=True)

    kills: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deaths: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assists: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    headshots: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    adr: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    kast: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    flank_kills: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_kill_distance: Mapped[float | None] = mapped_column(Float)
    time_alive: Mapped[float | None] = mapped_column(Float)
    travelled_distance: Mapped[float | None] = mapped_column(Float)

    played_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    player: Mapped["Player"] = relationship("Player", back_populates="match_stats")
