from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import config
from database.models import Base, Lead

engine = create_async_engine(config.database_url, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_lead_to_db(lead_data: dict) -> Lead:
    async with async_session_factory() as session:
        new_lead = Lead(
            telegram_id=lead_data["telegram_id"],
            username=lead_data.get("username"),
            phone=lead_data["phone"],
            language=lead_data.get("lang", "ru"),
            intent=lead_data["intent"],
            property_type=lead_data["property_type"],
            districts=lead_data.get("districts", ["Any"]),
            min_price_eur=lead_data["min_price"],
            max_price_eur=lead_data["max_price"],
            raw_query=lead_data.get("raw_query")
        )
        session.add(new_lead)
        await session.commit()
        await session.refresh(new_lead)
        return new_lead