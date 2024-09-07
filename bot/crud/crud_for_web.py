from datetime import timedelta, datetime 
from typing import Optional, List, Union, Type 
 
from sqlalchemy import select, or_, and_ 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload 
 
from bot.core.utils import moscow_now 
from bot.models.base import AsyncSessionLocal 
from bot.models.defect_model import EventType, Event 
from bot.models.models import Robot, MOSCOW_TZ, Gaz, UserWAAMer, Tip, Wire, Nozzle, Diffuser, Mudguard, Intestine, Rolls 
 
 
today_start = datetime.combine(datetime.today(), datetime.min.time()) 
tomorrow_start = today_start + timedelta(days=1) 
 
# Calculate the start of "yesterday" 
yesterday_start = today_start - timedelta(days=1) 
 
 
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
            or_(Event.event_type == 'SETTING', Event.event_type == 'CLEANING')& 
            and_( 
                Event.datarime >= yesterday_start, 
                Event.datarime < tomorrow_start 
            ) 
        ).order_by(Event.datarime.desc()) 
        result = await session.execute(query) 
        events = result.scalars().all() 
    return events 
 
 
async def not_standart_event(number): 
    async with AsyncSessionLocal() as session: 
        query = select(Event).join(Robot, Event.robot_id == Robot.id).options( 
            selectinload(Event.user) 
        ).where( 
            (Robot.robot_number == number) & (Event.event_type == 'DEFECT')& 
            and_( 
                Event.datarime >= yesterday_start, 
                Event.datarime < tomorrow_start 
            ) 
        ).order_by(Event.datarime.desc()) 
        result = await session.execute(query) 
        events = result.scalars().all() 
    return events
