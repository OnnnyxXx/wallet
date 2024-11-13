from typing import Union

from scr.wallets.models import Wallet
from scr.wallets.schemas import Operation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_wallet(session: AsyncSession, uuid: str) -> Wallet:
    """
    Gets a wallet from a session by UUID

    :param session: Asynchronous SQLAlchemy session
    :param uuid: Unique wallet identifier
    :return: The wallet or none if not found
    """

    result = await session.execute(select(Wallet).where(Wallet.uuid == uuid))
    return result.scalars().first()


async def create_wallet(session: AsyncSession, uuid: str) -> Wallet:
    """
    Creates a new wallet and adds it to the database.

    :param session: Asynchronous SQLAlchemy session
    :param uuid: Unique identifier for the new wallet
    :return: The created wallet
    """
    wallet = Wallet(uuid=uuid, balance=0.0)
    session.add(wallet)
    return wallet
    # async with session.begin():
    #     wallet = Wallet(uuid=uuid, balance=0.0)
    #     session.add(wallet)
    #     await session.commit()
    #     return wallet


async def update_wallet(session: AsyncSession, uuid: str, operation: Operation) -> Union[Wallet | str | None]:
    """
    So, here we carry out operations and at the same time check the balance, if the user wants to transfer an amount\
    that is not on his balance.

    :param session: Asynchronous SQLAlchemy session
    :param uuid: Unique wallet identifier
    :param operation: Operation containing the operation type and amount
    :return: We update the wallet and return it or messages Insufficient funds
    """
    wallet = await get_wallet(session, uuid)
    if not wallet:
        return None

    if operation.operationType == "DEPOSIT":
        wallet.balance += operation.amount
    elif operation.operationType == "WITHDRAW":
        if wallet.balance < operation.amount:
            return 'Insufficient funds'
        wallet.balance -= operation.amount

    await session.commit()
    await session.refresh(wallet)
    return wallet
