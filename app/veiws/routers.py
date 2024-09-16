from fastapi import APIRouter

from main import logger
from .router.index import router as index_rout
from .router.cell import router as cell_rout
from .router.table import router as table

main_router = APIRouter()

logger.info("Index router registered")
main_router.include_router(index_rout)
main_router.include_router(cell_rout)
main_router.include_router(table)
