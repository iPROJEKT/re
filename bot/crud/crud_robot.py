from typing import Optional, List, Union, Type

from sqlalchemy import distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.core.utils import moscow_now
from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import EventType, Event
from bot.models.models import Robot, MOSCOW_TZ, Gaz, UserWAAMer, Tip, Wire, Nozzle, Diffuser, Mudguard, Intestine, Rolls


async def get_multi_robot() -> list[Robot]:
    """
    Retrieve all robots from the database.

    Uses a session to query for all Robot objects, including related data
    such as wires, gases, and tips.

    Returns:
        list[Robot]: A list of Robot objects.
    """
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
        )
        result = await session.execute(query)
        robots = result.scalars().all()
        return robots


async def create_event(
    session: AsyncSession,
    user_id: int,
    event_type: EventType,
    additional_data: dict,
    robot_id: Optional[int] = None
) -> Event:
    """
    Create and store a new event in the database.

    Args:
        session (AsyncSession): The SQLAlchemy session to use for the operation.
        user_id (int): The ID of the user associated with the event.
        event_type (EventType): The type of the event.
        additional_data (dict): Additional data to be stored with the event.
        robot_id (Optional[int]): Optional ID of the robot associated with the event.

    Returns:
        Event: The created Event object.
    """
    event = Event(
        event_type=event_type,
        user_id=user_id,
        robot_id=robot_id,
        **additional_data
    )
    session.add(event)
    await session.commit()
    return event


async def get_multi_gaz(gaz_type: str) -> List[Gaz]:
    """
    Retrieve a list of gases based on their type.

    Args:
        gaz_type (str): The type of gas to retrieve.

    Returns:
        List[Gaz]: A list of Gaz objects matching the specified type.
    """
    async with AsyncSessionLocal() as session:
        query = select(Gaz).where(Gaz.gaz_type_obj == gaz_type)
        result = await session.execute(query)
        gases = result.scalars().all()
    return gases


async def update_cryo(user: UserWAAMer, gaz_id: int) -> None:
    """
    Update the cryo box (kreeobac) associated with a robot.

    Args:
        user (UserWAAMer): The user associated with the robot.
        gaz_id (int): The ID of the new cryo box gas.

    Updates the cryo box gas and last update time for the specified robot.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Robot).filter(
                Robot.robot_number == user.number_robot
            )
            result = await session.execute(stmt)
            robot = result.scalars().first()

            if robot:
                robot.robot_last_update_gaz = moscow_now(MOSCOW_TZ)
                robot.robot_gaz_id = gaz_id
                session.add(robot)


async def update_gaz(user: UserWAAMer, gaz_id: int, gas_type: str) -> None:
    """
    Update the gas associated with a robot.

    Args:
        user (UserWAAMer): The user associated with the robot.
        gaz_id (int): The ID of the new gas.
        gas_type (str): The type of the gas being updated ('Основной' or 'Дополнительный').

    Updates the gas and last update time for the specified robot based on the gas type.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Robot).filter(
                Robot.robot_number == user.number_robot
            )
            result = await session.execute(stmt)
            robot = result.scalars().first()

            if robot:
                if gas_type == 'Основной':
                    robot.robot_last_update_gaz = moscow_now(MOSCOW_TZ)
                    robot.robot_gaz_id = gaz_id
                elif gas_type == 'Дополнительный':
                    robot.robot_last_update_add_gaz = moscow_now(MOSCOW_TZ)
                    robot.robot_add_gaz_id = gaz_id
                session.add(robot)


async def get_multi_model(
    model: Type[
        Union[
            Tip, Gaz, Wire,
            Nozzle, Diffuser, Mudguard,
            Intestine, Rolls
        ]
    ]
) -> list[
    Union[
        Tip, Gaz, Wire,
        Nozzle, Diffuser, Mudguard,
        Intestine, Rolls
    ]
]:
    """
    Retrieve all records from the specified model.

    This function takes a model type as an argument and retrieves all the
    records of that model from the database.

    Args:
        model (Type[Union[Tip, Gaz, Wire, Nozzle, Diffuser, Mudguard, Intestine, Rolls]]):
            The SQLAlchemy model class from which to retrieve records.

    Returns:
        List[Union[Tip, Gaz, Wire, Nozzle, Diffuser, Mudguard, Intestine, Rolls]]:
            A list of instances of the specified model.
    """
    async with AsyncSessionLocal() as session:
        query = select(model)
        result = await session.execute(query)
        models = result.scalars().all()
    return models


async def update_robot_component(
    user: UserWAAMer,
    component_id: int,
    component_field: str,
    update_time_field: str,
    extra_fields: Optional[dict] = None
) -> None:
    """
    Updates a specific component, its last update time, and optionally additional fields for the robot associated with the given user.

    This function retrieves the robot associated with the user's installation number
    (`user.number_robot`) and updates the specified component, its last update time,
    and any additional fields provided in `extra_fields`.

    Args:
    - user (UserWAAMer): The user associated with the robot.
    - component_id (int): The ID of the new component to be set.
    - component_field (str): The name of the field in the Robot model to update with the component ID.
    - update_time_field (str): The name of the field in the Robot model to update with the current time.
    - extra_fields (dict, optional): Additional fields and their values to update in the Robot model.

    Returns:
    - None
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Robot).filter(
                Robot.robot_number == user.number_robot
            )
            result = await session.execute(stmt)
            robot = result.scalars().first()

            if robot:
                setattr(robot, component_field, component_id)
                setattr(robot, update_time_field, moscow_now(MOSCOW_TZ))

                if extra_fields:
                    for field, value in extra_fields.items():
                        setattr(robot, field, value)

                session.add(robot)


async def get_all_diameter(model):
    async with AsyncSessionLocal() as session:
        query = select(distinct(model.wire_diameter))
        result = await session.execute(query)
    return result.scalars().all()


async def get_all_wire_diameter(diam: float):
    async with AsyncSessionLocal() as session:
        query = select(Wire).where(Wire.wire_diameter == diam)
        result = await session.execute(query)
    return result.scalars().all()


async def get_wire_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Wire.wire_mark).where(Wire.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_gaz_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Gaz.gaz_name).where(Gaz.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_tip_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Tip.tip_type).where(Tip.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_rolls_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Rolls.rolls_cutout_type).where(Rolls.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_intestine_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Intestine.intestine_color).where(Intestine.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_diffuser_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Diffuser.diffuser_thread).where(Diffuser.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_mudguard_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Mudguard.mudguard_material).where(Mudguard.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_nozzle_name(item_id):
    async with AsyncSessionLocal() as session:
        query = select(Nozzle.nozzle_form).where(Nozzle.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()