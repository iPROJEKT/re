from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.models.base import AsyncSessionLocal
from bot.models.models import Robot


async def get_robot_web_socket(numbers: list[int]):
    contexts = {}
    for number in numbers:
        async with AsyncSessionLocal() as session:
            query = select(Robot).options(
                selectinload(Robot.robot_wire),
            ).where(
                Robot.robot_number == number
            )
            result = await session.execute(query)
            robot = result.scalar_one_or_none()

            if robot:
                contexts[number] = {
                    'wire': robot.robot_wire.wire_mark,
                    'wire_diameter': robot.robot_wire.wire_diameter,
                }

    return contexts
