from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import Event
from bot.models.models import Robot, Control


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


async def get_wire_replacements_by_mark(number):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(
                func.date(Event.datarime).label('replacement_date'),  # Дата замены (без времени)
                Event.message,  # Сообщение с описанием замены
                func.count(Event.id).label('replacement_count')  # Количество замен
            ).join(
                Robot, Event.robot_id == Robot.id
            ).where(
                (Robot.robot_number == number) &
                Event.message.like('Замена проволоки на %')
            )  # Фильтруем только замены проволоки
            .group_by(func.date(Event.datarime), Event.message)  # Группируем по дате и марке проволоки
            .order_by(func.date(Event.datarime).asc())  # Сортируем по дате замены
        )
        replacements = result.fetchall()
        return [
            {
                "replacement_date": row[0],
                "wire_mark": row[1].replace('Замена проволоки на ', ''),  # Извлекаем марку проволоки
                "replacement_count": row[2]
            }
            for row in replacements
        ]


async def get_tip_replacements_by_mark(number):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(
                func.date(Event.datarime).label('replacement_date'),  # Дата замены (без времени)
                Event.message,  # Сообщение с описанием замены
                func.count(Event.id).label('replacement_count')  # Количество замен
            ).join(
                Robot, Event.robot_id == Robot.id
            ).where(
                (Robot.robot_number == number) &
                Event.message.like('Замена наконечника на %')
            )  # Фильтруем только замены наконечников
            .group_by(func.date(Event.datarime), Event.message)  # Группируем по дате и марке наконечника
            .order_by(func.date(Event.datarime).asc())  # Сортируем по дате замены
        )
        replacements = result.fetchall()
        return [
            {
                "replacement_date": row[0],
                "tip_mark": row[1].replace('Замена наконечника на ', ''),  # Извлекаем марку наконечника
                "replacement_count": row[2]
            }
            for row in replacements
        ]


async def get_control_data(session: AsyncSession, component_type: str):
    """
    Функция для получения данных из таблицы Control по типу компонента (газ, наконечник, проволока).

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        component_type (str): Тип компонента (газ/наконечник/проволока).

    Returns:
        List[Dict]: Список данных в формате [{"name": ..., "count": ..., "start_count": ...}]
    """
    # Создаем SQL-запрос для получения данных из таблицы Control
    query = select(Control).where(Control.type == component_type)
    result = await session.execute(query)
    controls = result.scalars().all()

    control_data = [
        {
            "name": control.mark,
            "count": control.count,
            "start_count": control.start_count,
            "sub": control.sub
        }
        for control in controls
    ]

    return control_data
