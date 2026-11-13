from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, String, Integer, Text, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(50))
    language: Mapped[str] = mapped_column(String(5))

    intent: Mapped[str] = mapped_column(String(20))
    property_type: Mapped[str] = mapped_column(String(30))
    districts: Mapped[List[str]] = mapped_column(ARRAY(String))
    min_price_eur: Mapped[int] = mapped_column(Integer)
    max_price_eur: Mapped[int] = mapped_column(Integer)
    raw_query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )