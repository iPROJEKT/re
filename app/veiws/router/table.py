import asyncio
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect

from bot.crud.crud_for_web_socked import get_robot_web_socket
from bot.crud.crud_user import get_last_rb

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/table", response_class=HTMLResponse)
async def table_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="curent_statictic.html",
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            robots = await get_robot_web_socket([1, 2])
            now = datetime.now().strftime("%H:%M:%S")
            man = await get_last_rb()
            message = {
                'man': man,
                "time": now,
                "robots": robots,
            }

            # Отправляем данные в формате JSON
            await websocket.send_json(message)

            # Задержка в 1 секунду
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")
