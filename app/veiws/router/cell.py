import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket

from app.core.utils import get_common_event, get_common_contex
from bot.crud.crud_for_web import change_gaz, get_changes_by_day
from bot.crud.crud_for_web_socked import get_wire_replacements_by_mark, get_tip_replacements_by_mark

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/cell/{cell_id}", response_class=HTMLResponse)
async def cell_page(request: Request, cell_id: int):
    context = await get_common_event(cell_id)
    return templates.TemplateResponse(
        request=request,
        name=f"cell_{cell_id}.html",
        context=context
    )


@router.websocket('/ws/robot-state/{cell_id}')
async def websocket_robot(websocket: WebSocket, cell_id: int):
    await websocket.accept()
    while True:
        try:
            # Получаем актуальные данные о состоянии робота
            context = await get_common_contex(cell_id)

            # Преобразуем данные в JSON формат
            data_json = json.dumps(context)

            # Отправляем данные клиенту через WebSocket
            await websocket.send_text(data_json)

            # Задержка между обновлениями
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-data/{cell_id}")
async def websocket_endpoint(websocket: WebSocket,  cell_id: int):
    await websocket.accept()
    while True:
        try:
            ware_data = await get_changes_by_day(cell_id, 'Замена проволоки%', 'SETTING')
            tip_data = await get_changes_by_day(cell_id, 'Замена наконечника%', 'SETTING')
            gaz_data = await change_gaz(cell_id)
            rolls_data = await get_changes_by_day(cell_id, 'Замена роликов на%', 'SETTING')
            intestine_data = await get_changes_by_day(cell_id, 'Замена направляющего канала на%', 'SETTING')
            diffuser_data = await get_changes_by_day(cell_id, 'Замена диффузора на%', 'SETTING')
            mudguard_data = await get_changes_by_day(cell_id, 'Замена брызговика на%', 'SETTING')
            nozzle_data = await get_changes_by_day(cell_id, 'Замена сопла на%', 'SETTING')

            ware_data_by_day = [(row.date, row.count) for row in ware_data]
            tip_data_by_day = [(row.date, row.count) for row in tip_data]
            gaz_data_by_day = [(row.date, row.count) for row in gaz_data]
            rolls_data_by_day = [(row.date, row.count) for row in rolls_data]
            intestine_data_by_day = [(row.date, row.count) for row in intestine_data]
            diffuser_data_by_day = [(row.date, row.count) for row in diffuser_data]
            mudguard_data_by_day = [(row.date, row.count) for row in mudguard_data]
            nozzle_data_by_day = [(row.date, row.count) for row in nozzle_data]

            data = {
                'ware_data': ware_data_by_day,
                'tip_data': tip_data_by_day,
                'gaz_data': gaz_data_by_day,
                'rolls_data': rolls_data_by_day,
                'intestine_data': intestine_data_by_day,
                'diffuser_data': diffuser_data_by_day,
                'mudguard_data': mudguard_data_by_day,
                'nozzle_data': nozzle_data_by_day
            }
            data_json = json.dumps(data)
            await websocket.send_text(data_json)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-wire-data/{cell_id}")
async def websocket_endpoint_wire(websocket: WebSocket, cell_id: int):
    await websocket.accept()
    while True:
        try:
            wire_brands = [
                'Св-08Г2С-О', 'Св-АМг6', 'Св-04Х19Н9', 'Св-06х19н9т',
                'Св-12х13', 'Св-08Г2С ультра', 'Св-Г2СНТ-О', 'Ultra 700',
                'Ultra 500', '30ХГСА', 'Св-01Х23Н28М3Д3', 'Св-08ЧГСМФА-О',
                'Св-08Г2С-Br'
            ]

            wire_data = {}

            for brand in wire_brands:
                data = await get_changes_by_day(cell_id, f'Замена проволоки на {brand}%', 'SETTING')
                wire_data_by_day = [(row.date, row.count) for row in data]
                wire_data[brand] = wire_data_by_day

            data_json = json.dumps(wire_data)
            await websocket.send_text(data_json)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-tip-data/{cell_id}")
async def websocket_endpoint_tip(websocket: WebSocket, cell_id: int):
    await websocket.accept()
    while True:
        try:
            tip_diameters = ['0.8', '1.0', '1.2', '1.6']
            tip_data = {}
            for diameter in tip_diameters:
                data = await get_changes_by_day(cell_id, f'Замена наконечника на {diameter}%', 'SETTING')
                tip_data_by_day = [(row.date, row.count) for row in data]
                tip_data[diameter] = tip_data_by_day

            data_json = json.dumps(tip_data)
            await websocket.send_text(data_json)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-gas-data/{cell_id}")
async def websocket_endpoint_gas(websocket: WebSocket, cell_id: int):
    await websocket.accept()
    while True:
        try:
            gas_types = {
                'Замена основной газа на Ar-98% CO2-2%': 6400,  # 1 замена = 6400 л
                'Замена креобака на газ Ar 100%': 27 * 6400,  # 1 замена = 27 * 6400 л
                'Замена основной газа на Ar 100%': 6400,  # 1 замена = 6400 л
                'Замена дополнительный газа на ID Ar 100%': 6400  # 1 замена = 6400 л
            }

            gas_data = {}
            for gas_type, coefficient in gas_types.items():
                data = await get_changes_by_day(cell_id, gas_type, 'SETTING')

                # Умножаем количество замен на соответствующий коэффициент объема
                gas_data_by_day = [(row.date, row.count * coefficient) for row in data]
                gas_data[gas_type] = gas_data_by_day

            # Преобразуем данные в JSON и отправляем по WebSocket
            data_json = json.dumps(gas_data)
            await websocket.send_text(data_json)

            # Задержка перед следующей отправкой
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-defect-data/{cell_id}")
async def websocket_endpoint_defects(websocket: WebSocket, cell_id: int):
    await websocket.accept()
    while True:
        try:
            defects = [
                'Деформации',
                'Поры',
                'Несплавления',
                'Подрезы',
                'Трещины',
                'Прожиг',
                'Заплавленый наконечник'
            ]

            defect_data = {}
            for defect_name in defects:
                data = await get_changes_by_day(cell_id, f'{defect_name}%', 'DEFECT')
                defect_data_by_day = [(row.date, row.count) for row in data]

                # Записываем данные для каждого дефекта в словарь
                defect_data[defect_name] = defect_data_by_day

            data_json = json.dumps(defect_data)
            await websocket.send_text(data_json)

            # Задержка перед следующим циклом
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break