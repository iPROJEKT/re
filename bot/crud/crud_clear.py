from sqlalchemy.future import select

from bot.core.utils import moscow_now
from bot.models.base import AsyncSessionLocal
from bot.models.models import UserWAAMer, Robot, MOSCOW_TZ


async def clear_robot_component(user: UserWAAMer, clear_component: str) -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Robot).filter(
                Robot.robot_number == user.number_robot
            )
            result = await session.execute(stmt)
            robot = result.scalars().first()

            if robot:
                setattr(robot, clear_component, moscow_now(MOSCOW_TZ))

            session.add(robot)
