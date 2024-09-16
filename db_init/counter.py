import asyncio

from bot.models.base import AsyncSessionLocal
from bot.models.models import Control


async def create_control_data():
    # Данные для наконечников
    tip_data = [
        {'type': 'наконечник', 'mark': 'Cu-Cr-Zr', 'sub': '0.8', 'count': 1},
        {'type': 'наконечник', 'mark': 'Cu-Cr-Zr', 'sub': '1.0', 'count': 2},
        {'type': 'наконечник', 'mark': 'Cu-Cr-Zr', 'sub': '1.2', 'count': 3},
        {'type': 'наконечник', 'mark': 'Cu-Cr-Zr', 'sub': '1.6', 'count': 4},
    ]

    # Данные для проволок
    wire_data = [
        {'type': 'проволока', 'mark': 'Св-08Г2С-О', 'sub': '1.2', 'count': 1},
        {'type': 'проволока', 'mark': 'Св-АМг6', 'sub': '0.8', 'count': 3},
        {'type': 'проволока', 'mark': 'Св-08Г2С-О', 'sub': '0.8', 'count': 4},
        {'type': 'проволока', 'mark': 'Св-08Г2С-О', 'sub': '1.0', 'count': 5},
        {'type': 'проволока', 'mark': 'Св-04Х19Н9', 'sub': '1.0', 'count': 6},
        {'type': 'проволока', 'mark': 'Св-06х19н9т', 'sub': '1.0', 'count': 7},
        {'type': 'проволока', 'mark': 'Св-06х19н9т', 'sub': '1.2', 'count': 8},
        {'type': 'проволока', 'mark': 'Св-12х13', 'sub': '1.2', 'count': 9},
        {'type': 'проволока', 'mark': 'Св-08Г2С ультра', 'sub': '1.6', 'count': 10},
        {'type': 'проволока', 'mark': 'Св-Г2СНТ-О', 'sub': '1.0', 'count': 11},
        {'type': 'проволока', 'mark': 'Ultra 700', 'sub': '1.2', 'count': 12},
        {'type': 'проволока', 'mark': 'Ultra 500', 'sub': '1.2', 'count': 13},
        {'type': 'проволока', 'mark': '30ХГСА', 'sub': '1.2', 'count': 14},
        {'type': 'проволока', 'mark': 'Св-01Х23Н28М3Д3', 'sub': '1.2', 'count': 16},
        {'type': 'проволока', 'mark': 'Св-08ЧГСМФА-О', 'sub': '1.2', 'count': 17},
        {'type': 'проволока', 'mark': 'Св-08Г2С', 'sub': '1.2', 'count': 18},
        {'type': 'проволока', 'mark': 'Св-08Г2С-Br', 'sub': '1.2', 'count': 19},
    ]

    # Данные для газа
    gaz_data = [
        {'type': 'газ', 'mark': 'Ar 100%', 'sub': 'Баллон', 'count': 1},
        {'type': 'газ', 'mark': 'Ar 100%', 'sub': 'Креобак', 'count': 2},
        {'type': 'газ', 'mark': 'Ar-98% CO2-2%', 'sub': 'Баллон', 'count': 3},
        {'type': 'газ', 'mark': 'Ar-80% CO2-20%', 'sub': 'Баллон', 'count': 4},
        {'type': 'газ', 'mark': 'CO2 100%', 'sub': 'Баллон', 'count': 5},
        {'type': 'газ', 'mark': 'He 100%', 'sub': 'Баллон', 'count': 6},
    ]

    # Объединение всех данных
    control_data = tip_data + wire_data + gaz_data

    # Добавление всех записей в базу данных
    created_controls = []
    async with AsyncSessionLocal() as session:
        for data in control_data:
            new_control = Control(
                type=data['type'],
                mark=data['mark'],
                sub=data['sub'],
                count=data['count']
            )
            session.add(new_control)
            created_controls.append(new_control)

    # Сохранение изменений
    await session.commit()
    print(created_controls)


async def main():
    await create_control_data()


asyncio.run(main())
