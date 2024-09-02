import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.core import app
from bot.core.const import LOG_FORM, LOG_FILEMOD, LOG_FILENAME
from bot.handlers import (
    start_menu, register_handler,
    state_robot, get_cell_for_work,
    standard_events, cleaning_event,
    abnormal_events
)

load_dotenv()

logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


async def start_fastapi():
    import uvicorn
    from app.admin.admin import admin
    from app.veiws.index import router
    app.mount("/admin", admin)
    app.include_router(router)
    config = uvicorn.Config(app, host="192.168.20.152", port=8080, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        start_menu.router,
        register_handler.router,
        state_robot.router,
        get_cell_for_work.router,
        standard_events.router,
        cleaning_event.router,
        abnormal_events.router,

    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(start_bot(), start_fastapi())

if __name__ == '__main__':
    logging.basicConfig(
        format=LOG_FORM,
        filemode=LOG_FILEMOD,
        filename=LOG_FILENAME,
        level=logging.INFO,
    )
    try:
        asyncio.run(main())
    except TokenValidationError as e:
        logger.error(f"Token validation failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
