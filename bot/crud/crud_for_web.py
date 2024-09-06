from typing import Optional, List, Union, Type

from sqlalchemy import or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.core.utils import moscow_now
from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import EventType, Event
from bot.models.models import Robot, MOSCOW_TZ, Gaz, UserWAAMer, Tip, Wire, Nozzle, Diffuser, Mudguard, Intestine, Rolls


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


async def change_wire(number):
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Event).join(Robot, Event.robot_id == Robot.id).where(
            (Robot.robot_number == number) &
            (Event.event_type == 'SETTING') &
            (Event.message.like('Замена проволоки%'))
        )
        result = await session.execute(query)
        count = result.scalar()
    return count


async def change_tip_c(number):
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Event).join(Robot, Event.robot_id == Robot.id).where(
            (Robot.robot_number == number) &
            (Event.event_type == 'SETTING') &
            (Event.message.like('Замена наконечника%'))
        )
        result = await session.execute(query)
        count = result.scalar()
    return count


async def def_cou(number):
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Event).join(Robot, Event.robot_id == Robot.id).where(
            (Robot.robot_number == number) &
            (Event.event_type == 'DEFECT')
        )
        result = await session.execute(query)
        count = result.scalar()
    return count
