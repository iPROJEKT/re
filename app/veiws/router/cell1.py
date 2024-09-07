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


@router.get("/cell-1", response_class=HTMLResponse)
async def cell_1_page(request: Request):
    context = await get_common_event(number=1)
    return templates.TemplateResponse(
        request=request,
        name="cell_1.html",
        context=context
    )


@router.websocket('/ws/robot-state/1')
async def websocket_robot(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Получаем актуальные данные о состоянии робота
            context = await get_common_contex(1)

            # Преобразуем данные в JSON формат
            data_json = json.dumps(context)

            # Отправляем данные клиенту через WebSocket
            await websocket.send_text(data_json)

            # Задержка между обновлениями
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            break



@router.websocket("/ws/tip-data/1")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            ware_data = await get_changes_by_day(1, 'Замена проволоки%')
            tip_data = await get_changes_by_day(1, 'Замена наконечника%')
            gaz_data = await change_gaz(1)
            rolls_data = await get_changes_by_day(1, 'Замена роликов на%')
            intestine_data = await get_changes_by_day(1, 'Замена направляющего канала на%')
            diffuser_data = await get_changes_by_day(1, 'Замена диффузора на%')
            mudguard_data = await get_changes_by_day(1, 'Замена брызговика на%')
            nozzle_data = await get_changes_by_day(1, 'Замена сопла на%')

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
