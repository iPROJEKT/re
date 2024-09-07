from fastapi import APIRouter

from .router.index import router as index_rout
from .router.cell1 import router as cell1_rout
from .router.cell2 import router as cell2_rout
from .router.table import router as table

main_router = APIRouter()

main_router.include_router(index_rout)
main_router.include_router(cell1_rout)
main_router.include_router(cell2_rout)
main_router.include_router(table)
