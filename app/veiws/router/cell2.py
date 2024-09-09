import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket

from app.core.utils import get_common_event, get_common_contex
from bot.crud.crud_for_web import change_gaz, get_changes_by_day

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/cell-2", response_class=HTMLResponse)
async def cell_2_page(request: Request):
    context = await get_common_event(number=2)
    return templates.TemplateResponse(
        request=request,
        name="cell_2.html",
        context=context
    )


@router.websocket('/ws/robot-state/2')
async def websocket_robot_2(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Получаем актуальные данные о состоянии робота
            context = await get_common_contex(2)

            # Преобразуем данные в JSON формат
            data_json = json.dumps(context)

            # Отправляем данные клиенту через WebSocket
            await websocket.send_text(data_json)

            # Задержка между обновлениями
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-data/2")
async def websocket_endpoint_2(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            ware_data = await get_changes_by_day(2, 'Замена проволоки%')
            tip_data = await get_changes_by_day(2, 'Замена наконечника%')
            gaz_data = await change_gaz(2)
            rolls_data = await get_changes_by_day(2, 'Замена роликов на%')
            intestine_data = await get_changes_by_day(2, 'Замена направляющего канала на%')
            diffuser_data = await get_changes_by_day(2, 'Замена диффузора на%')
            mudguard_data = await get_changes_by_day(2, 'Замена брызговика на%')
            nozzle_data = await get_changes_by_day(2, 'Замена сопла на%')

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


@router.websocket("/ws/all-wire-data/2")
async def websocket_endpoint_wire(websocket: WebSocket):
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
                data = await get_changes_by_day(2, f'Замена проволоки на {brand}%')
                wire_data_by_day = [(row.date, row.count) for row in data]
                wire_data[brand] = wire_data_by_day

            data_json = json.dumps(wire_data)
            await websocket.send_text(data_json)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break


@router.websocket("/ws/all-tip-data/2")
async def websocket_endpoint_tip(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            tip_diameters = ['0.8', '1.0', '1.2', '1.6']
            tip_data = {}
            for diameter in tip_diameters:
                data = await get_changes_by_day(2, f'Замена наконечника на {diameter}%')
                tip_data_by_day = [(row.date, row.count) for row in data]
                tip_data[diameter] = tip_data_by_day

            data_json = json.dumps(tip_data)
            await websocket.send_text(data_json)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break