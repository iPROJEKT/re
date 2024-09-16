from sqlalchemy import or_, func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import Event
from bot.models.models import Robot


async def get_robot(number):
    async with AsyncSessionLocal() as session:
        query = select(Robot).options(
            selectinload(Robot.robot_wire),
            selectinload(Robot.robot_gaz),
            selectinload(Robot.robot_add_gaz),
            selectinload(Robot.robot_tip),
            selectinload(Robot.robot_rolls),
            selectinload(Robot.robot_intestine),
            selectinload(Robot.robot_diffuser),
            selectinload(Robot.robot_mudguard),
            selectinload(Robot.robot_nozzle),
        ).where(
            Robot.robot_number == number
        )
        result = await session.execute(query)
        robot = result.scalar_one_or_none()
    return robot


async def standart_event(number):
    try:
        async with AsyncSessionLocal() as session:
            query = select(Event).join(Robot, Event.robot_id == Robot.id).options(
                selectinload(Event.user)
            ).where(
                (Robot.robot_number == number) &
                or_(Event.event_type == 'SETTING', Event.event_type == 'CLEANING')
            ).order_by(Event.datarime.desc())
            result = await session.execute(query)
            events = result.scalars().all()
        return events
    except Exception as e:
        print(f"Error executing query: {e}")
        raise


async def not_standart_event(number):
    async with AsyncSessionLocal() as session:
        query = select(Event).join(Robot, Event.robot_id == Robot.id).options(
            selectinload(Event.user)
        ).where(
            (Robot.robot_number == number) & (Event.event_type == 'DEFECT')
        ).order_by(Event.datarime.desc())
        result = await session.execute(query)
        events = result.scalars().all()
    return events


async def def_cou(number):
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Event).join(Robot, Event.robot_id == Robot.id).where(
            (Robot.robot_number == number) &
            (Event.event_type == 'DEFECT')
        )
        result = await session.execute(query)
        count = result.scalar()
    return count


async def change_gaz(number: int):
    async with AsyncSessionLocal() as session:
        query = select(
            func.date(Event.datarime).label('date'),
            func.count().label('count')
        ).select_from(Event).join(
            Robot, Event.robot_id == Robot.id
        ).where(
            (Robot.robot_number == number) &
            (
                Event.message.like('Замена основной газа на%') |
                Event.message.like('Замена креобака на%') |
                Event.message.like('Замена дополнительный газа на%')
            ) &
            (Event.event_type == 'SETTING')
        ).group_by(
            func.date(Event.datarime)
        )

        result = await session.execute(query)
        changes_by_day = result.all()
    return changes_by_day


async def get_changes_by_day(number: int, message_like: str, event_type: str):
    async with AsyncSessionLocal() as session:
        query = select(
            func.date(Event.datarime),
            func.count()
        ).select_from(Event).join(
            Robot, Event.robot_id == Robot.id
        ).where(
            (Robot.robot_number == number) &
            (Event.event_type == event_type) &
            (Event.message.like(message_like))
        ).group_by(
            func.date(Event.datarime)
        )
        result = await session.execute(query)
        changes_by_day = result.all()
    return changes_by_day