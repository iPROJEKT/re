import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.base import AsyncSessionLocal
from bot.models.models import Wire, Intestine, Rolls, Tip, Gaz, Robot


async def populate_wire_data():
    """Наполнение базы проволокой"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            wires = [
                Wire(wire_mark='Св-08Г2С-О', wire_diameter=1.2),
                Wire(wire_mark='Св-08Г2С-О', wire_diameter=1.2),
                Wire(wire_mark='Св-АМг6', wire_diameter=0.8),
                Wire(wire_mark='Св-08Г2С-О', wire_diameter=0.8),
                Wire(wire_mark='Св-08Г2С-О', wire_diameter=1.0),
                Wire(wire_mark='Св-04Х19Н9', wire_diameter=1.0),
                Wire(wire_mark='Св-06х19н9т', wire_diameter=1.0),
                Wire(wire_mark='Св-06х19н9т', wire_diameter=1.2),
                Wire(wire_mark='Св-12х13', wire_diameter=1.2),
                Wire(wire_mark='Св-08Г2С ультра', wire_diameter=1.6),
                Wire(wire_mark='Св-Г2СНТ-О', wire_diameter=1.0),
                Wire(wire_mark='Ultra 700', wire_diameter=1.2),
                Wire(wire_mark='Ultra 500', wire_diameter=1.2),
                Wire(wire_mark='30ХГСА', wire_diameter=1.2),
                Wire(wire_mark='12Х18Н10Т', wire_diameter=1.0),
                Wire(wire_mark='Св-01Х23Н28М3Д3', wire_diameter=1.2),
                Wire(wire_mark='Св-08ЧГСМФА-О', wire_diameter=1.2),
                Wire(wire_mark='Св-08Г2С', wire_diameter=1.2),
                Wire(wire_mark='Св-08Г2С-Br', wire_diameter=1.2)
            ]
            session.add_all(wires)
        await session.commit()


async def populate_gaz_data():
    """Наполнение базы газами"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            gazes = [
                Gaz(gaz_name='Ar 100%', gaz_type_obj='Баллон'),
                Gaz(gaz_name='Ar 100%', gaz_type_obj='Креобак'),
                Gaz(gaz_name='Ar-98% CO2-2%', gaz_type_obj='Баллон'),
                Gaz(gaz_name='Ar-80% CO2-20%', gaz_type_obj='Баллон'),
                Gaz(gaz_name='CO2 100%', gaz_type_obj='Баллон'),
                Gaz(gaz_name='He 100%', gaz_type_obj='Баллон'),
            ]
            session.add_all(gazes)
        await session.commit()


async def populate_tip_data():
    """Наполнение базы наконечниками"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            tips = [
                Tip(tip_diameter=0.8, tip_type='Cu-Cr-Zr'),
                Tip(tip_diameter=1.0, tip_type='Cu-Cr-Zr'),
                Tip(tip_diameter=1.2, tip_type='Cu-Cr-Zr'),
                Tip(tip_diameter=1.6, tip_type='Cu-Cr-Zr'),
            ]
            session.add_all(tips)
        await session.commit()


async def add_rolls():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            rolls_data = [
                {"rolls_cutout_type": "V", "rolls_color": "Синий с красным", "rolls_ware_dim": "1.0-1.2 мм"},
                {"rolls_cutout_type": "U", "rolls_color": "Красный с желтым", "rolls_ware_dim": "1.2 мм"},
                {"rolls_cutout_type": "V", "rolls_color": "Синий", "rolls_ware_dim": "1 мм"},
                {"rolls_cutout_type": "U", "rolls_color": "Черный с желтым", "rolls_ware_dim": "1.6 мм"},
                {"rolls_cutout_type": "V", "rolls_color": "Черный", "rolls_ware_dim": "1.6 мм"},
            ]

            for data in rolls_data:
                new_roll = Rolls(**data)
                session.add(new_roll)


async def add_intestines():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            intestines_data = [
                {"intestine_color": "Синий", "intestine_diameter": "0.6-0.9", "intestine_length": 2.0},
                {"intestine_color": "Красный", "intestine_diameter": "1.0-1.2", "intestine_length": 2.0},
                {"intestine_color": "Желтый", "intestine_diameter": "1.2-1.6", "intestine_length": 2.0},
                {"intestine_color": "Зеленый", "intestine_diameter": "2.0 - 2.4", "intestine_length": 2.0},
                {"intestine_color": "Черный", "intestine_diameter": "1.2 - 1.6", "intestine_length": 2.0},
                {"intestine_color": "Черный", "intestine_diameter": "2.4", "intestine_length": 2.0},
                {"intestine_color": "Синий", "intestine_diameter": "3.2", "intestine_length": 2.0},
            ]

            for data in intestines_data:
                new_intestine = Intestine(**data)
                session.add(new_intestine)


async def populate_robots_data():
    """Наполнение базы роботами"""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(text("SELECT id FROM wire"))
            wires_ids = [row[0] for row in result]

            result = await session.execute(text("SELECT id FROM gaz"))
            gazes_ids = [row[0] for row in result]

            result = await session.execute(text("SELECT id FROM tip"))
            tips_ids = [row[0] for row in result]

            result = await session.execute(text("SELECT id FROM rolls"))
            rolls_ids = [row[0] for row in result]

            result = await session.execute(text("SELECT id FROM intestine"))
            intestines_ids = [row[0] for row in result]
            robots = [
                Robot(robot_number=1, robot_wire_id=wires_ids[0], robot_gaz_id=gazes_ids[0],
                      robot_add_gaz_id=gazes_ids[1], robot_tip_id=tips_ids[0], robot_rolls_id=rolls_ids[0],
                      robot_intestine_id=intestines_ids[0]),
                Robot(robot_number=2, robot_wire_id=wires_ids[1], robot_gaz_id=gazes_ids[1],
                      robot_add_gaz_id=gazes_ids[2], robot_tip_id=tips_ids[1], robot_rolls_id=rolls_ids[1],
                      robot_intestine_id=intestines_ids[1])
            ]
            session.add_all(robots)
        await session.commit()


async def main():
    await populate_wire_data()
    await populate_gaz_data()
    await populate_tip_data()
    await add_rolls()
    await add_intestines()
    await populate_robots_data()


asyncio.run(main())
