import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket

from bot.crud.crud_for_web_socked import get_control_data
from bot.models.base import AsyncSessionLocal

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def hello_world(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.websocket('/ws/material/control/')
async def index_material(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Получаем сообщение от клиента
            message = await websocket.receive_text()
            request_data = json.loads(message)
            component_type = request_data.get("type", "проволока")

            async with AsyncSessionLocal() as session:
                # Получаем данные для всех типов компонентов
                wire_data = await get_control_data(session, "проволока")
                tip_data = await get_control_data(session, "наконечник")
                gas_data = await get_control_data(session, "газ")

            # Отправляем данные для всех типов
            await websocket.send_text(json.dumps({
                "wire_data": wire_data,
                "tip_data": tip_data,
                "gas_data": gas_data,
            }))
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break