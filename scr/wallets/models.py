from sqlalchemy import Column, String, Float

from database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    uuid = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0.0)


async def create_tables(engine):
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы.")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")