from sqlalchemy import select

from bot.models.base import AsyncSessionLocal
from bot.models.models import UserWAAMer, Table


async def create_user(
    telegram_user_id: int,
    name: str,
    surname: str,
    is_admin: bool = False,
) -> None:
    """
    Creates a new user in the database.

    :param telegram_user_id: int
        The user's Telegram ID.
    :param name: str
        The user's first name.
    :param surname: str
        The user's last name.
    :param is_admin: bool, optional
        A flag indicating whether the user is an administrator (default is False).
    :return: None
    """
    result = UserWAAMer(
        telegram_user_id=telegram_user_id,
        name=name,
        surname=surname,
        is_admin=is_admin
    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)


async def get_user_by_id(telegram_id: int) -> UserWAAMer:
    """
    Retrieves a user by their Telegram ID.

    :param telegram_id: int
        The user's Telegram ID.
    :return: UserWAAMer or None
        The user object if found, otherwise None.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserWAAMer).where(
                UserWAAMer.telegram_user_id == telegram_id
            )
        )
        return result.scalar_one_or_none()


async def is_admin(telegram_id: int) -> bool:
    """
    Checks if a user is an administrator.

    :param telegram_id: int
        The user's Telegram ID.
    :return: bool
        True if the user is an administrator, otherwise False.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserWAAMer.is_admin).where(
                UserWAAMer.telegram_user_id == telegram_id
            )
        )
        return result.scalar_one_or_none()


async def is_collector(telegram_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserWAAMer.is_collector).where(
                UserWAAMer.telegram_user_id == telegram_id
            )
        )
        return result.scalar_one_or_none()


async def cell_for_user(
    user: UserWAAMer,
    cell_number: int
) -> None:
    """
     Assigns a robot cell number to a user.

     :param user: UserWAAMer
         The user object to assign the cell number to.
     :param cell_number: int
         The cell number to be assigned.
     :return: None
     """
    async with AsyncSessionLocal() as session:
        user.number_robot = cell_number
        session.add(user)
        await session.commit()


async def get_last_rb():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Table).order_by(Table.id.desc()).limit(1))
        last_record = result.scalars().first()  # Получаем последнюю запись
        return last_record
