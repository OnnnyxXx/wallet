from scr.wallets.crud import update_wallet, get_wallet, create_wallet
from scr.wallets.models import Wallet
from scr.wallets.schemas import Operation
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker

router = APIRouter(
    tags=['Wallet']
)


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.post("/api/v1/wallets/")
async def create_wallets(uuid: str):
    """
    :param uuid:
        Create unique wallet identifier

    :return:
        A new wallet and balance or messages with -> Wallet already exists
    """
    async with async_session_maker() as session:
        try:
            check_wallet = await get_wallet(session, uuid)
            if check_wallet:
                raise HTTPException(status_code=400, detail="Wallet already exists")

            wallet = await create_wallet(session, uuid)
            await session.commit()
            return {"uuid": wallet.uuid, "balance": wallet.balance}
        except Exception as er:
            raise HTTPException(status_code=500, detail=str(er))


@router.post("/api/v1/wallets/{uuid}/operation")
async def perform_operation(uuid: str, operation: Operation, db: AsyncSession = Depends(get_db)):
    """
    :param uuid:
        Unique wallet identifier

    :param operation:
        Operation containing the operation type and amount

    :param db:
        Asynchronous SQLAlchemy

    :return:
        uuid and balance or Insufficient funds or wallet not found
    """

    wallet = await update_wallet(db, uuid, operation)
    if not wallet:
        raise HTTPException(status_code=400, detail="Insufficient funds or wallet not found")
    return {"uuid": wallet.uuid, "balance": wallet.balance}


@router.get('/api/v1/wallets/{uuid}')
async def get_balance(uuid: str, db: AsyncSession = Depends(get_db)):
    """
    :param uuid:
        Unique wallet identifier

    :param db:
        Asynchronous SQLAlchemy

    :return:
        uuid and balance or Wallet not found
    """
    wallet = await get_wallet(db, uuid)
    if not wallet:
        raise HTTPException(status_code=400, detail="Wallet not found")
    return {"uuid": wallet.uuid, "balance": wallet.balance}
