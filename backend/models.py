from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Room(Base):
    __tablename__ = "rooms"

    code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    p1_id: Mapped[str | None] = mapped_column(
        String(100)
    )

    p2_id: Mapped[str | None] = mapped_column(
        String(100)
    )

    is_p1_turn: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    num_messages: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # TODO: ADD FUNCTION SYMBOLS AND STUFF


class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    code : Mapped[str] = mapped_column(
        ForeignKey("rooms.code", ondelete="CASCADE")
    )

    player_id: Mapped[str] = mapped_column(
        String(100)
    )

    message: Mapped[str] = mapped_column(
        String(1000)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    
