from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel,Session
from .models import SQLModel,Shipment
from App.config import settings


engine= create_async_engine(
    url=settings.POSTGRES_URL,echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


# session = Session(bind=engine)                
# session.get(   
#     shipment,12701
# )

# session.add(shipment(id=12703))
# session.commit()

async def get_session():
    async_session= sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session



